use clap::{Parser, Subcommand};
use std::path::PathBuf;

mod ecs;
mod document;
mod config;
mod pipeline;
mod plugins;

#[derive(Parser)]
#[command(name = "docforge")]
#[command(about = "ECS-inspired document processing pipeline")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Process {
        #[arg(long)]
        input: PathBuf,
        #[arg(long)]
        output: PathBuf,
    },
}

fn main() {
    env_logger::init();
    let cli = Cli::parse();

    match cli.command {
        Commands::Process { input, output } => {
            if let Err(e) = run_pipeline(input, output) {
                eprintln!("Pipeline error: {}", e);
                std::process::exit(1);
            }
        }
    }
}

fn run_pipeline(input: PathBuf, output: PathBuf) -> Result<(), Box<dyn std::error::Error>> {
    log::info!("Starting DocForge pipeline");
    log::info!("Input: {:?}, Output: {:?}", input, output);

    let mut store = ecs::EntityStore::new();
    let mut resources = ecs::ResourceMap::new();

    resources.insert(config::FontConfig::default());
    resources.insert(config::InputConfig::new(input.clone()));

    document::load_documents(&input, &mut store)?;
    log::info!("Loaded {} documents", store.all_entities().len());

    let mut runner = pipeline::PipelineRunner::new();

    runner.add_plugin(Box::new(plugins::font_normalizer::FontNormalizerPlugin));
    runner.add_plugin(Box::new(plugins::metadata_extractor::MetadataExtractorPlugin));
    runner.add_plugin(Box::new(plugins::template_expander::TemplateExpanderPlugin));
    runner.add_plugin(Box::new(plugins::crossref::CrossRefPlugin::new()));
    runner.add_plugin(Box::new(plugins::toc_generator::TocGeneratorPlugin));
    runner.add_plugin(Box::new(plugins::manifest_writer::ManifestWriterPlugin));

    runner.run(&mut store, &resources)?;

    log::info!("Pipeline completed successfully");
    Ok(())
}
