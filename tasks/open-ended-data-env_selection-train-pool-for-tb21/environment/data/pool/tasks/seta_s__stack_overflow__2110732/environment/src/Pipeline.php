<?php

class Pipeline
{
    private Database $db;
    private ContentProcessor $processor;
    private Logger $logger;

    public function __construct()
    {
        $this->logger = new Logger();
        $this->db = new Database();
        $this->processor = new ContentProcessor();
    }

    public function run(): void
    {
        $this->logger->log("Pipeline started");

        if (!is_dir('/app/output')) {
            mkdir('/app/output', 0755, true);
        }

        $categories = $this->db->getAllCategories();
        $this->logger->log("Found " . count($categories) . " categories");

        $report = [];

        foreach ($categories as $category) {
            $this->logger->log("Processing category: $category");
            $records = $this->db->getRecordsByCategory($category);

            foreach ($records as $record) {
                $this->logger->log("Processing record: " . $record['title']);
                $links = $this->processor->extractLinks($record['html_body']);

                $report[] = [
                    'id' => (int) $record['id'],
                    'title' => $record['title'],
                    'category' => $record['category'],
                    'links' => $links,
                ];
            }
        }

        $jsonOutput = json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
        file_put_contents('/app/output/report.json', $jsonOutput);

        $this->logger->log("Pipeline completed. Report written with " . count($report) . " entries.");
    }
}
