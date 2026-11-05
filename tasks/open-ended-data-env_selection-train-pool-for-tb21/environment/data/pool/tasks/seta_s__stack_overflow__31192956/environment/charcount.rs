use std::fs::File;
use std::io::{self, BufReader, Read};

pub fn count_endpoint_chars(path: &str) -> Result<usize, io::Error> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut count = 0usize;

    for ch in reader.chars() {
        let c = ch.map_err(|e| io::Error::new(io::ErrorKind::Other, e.to_string()))?;
        if !c.is_whitespace() {
            count += 1;
        }
    }

    Ok(count)
}

pub fn count_with_read_until(path: &str) -> Result<usize, io::Error> {
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    let mut buf = Vec::new();
    let mut count = 0usize;

    loop {
        let bytes_read = reader.read_until(b'\n', &mut buf)?;
        if bytes_read == 0 {
            break;
        }
        let line = String::from_utf8_lossy(&buf);
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() >= 7 {
            let endpoint = parts[6];
            for ch in endpoint.chars() {
                if !ch.is_whitespace() {
                    count += 1;
                }
            }
        }
    }

    Ok(count)
}
