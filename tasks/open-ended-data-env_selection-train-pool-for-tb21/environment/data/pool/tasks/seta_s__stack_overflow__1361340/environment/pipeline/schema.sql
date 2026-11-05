CREATE TABLE IF NOT EXISTS transcripts (
    ensembl_transcript_id VARCHAR(20) NOT NULL,
    gene_id               VARCHAR(20) NOT NULL,
    chrom_start           INT UNSIGNED NOT NULL,
    chrom_end             INT UNSIGNED NOT NULL,
    PRIMARY KEY (ensembl_transcript_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS gene_annotations (
    id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    gene_id          VARCHAR(20)  NOT NULL,
    annotation_type  VARCHAR(50)  NOT NULL,
    annotation_value VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
