<?php

require_once __DIR__ . '/lib/AsymmetricCrypto.php';

$keysDir = __DIR__ . '/keys';

if ($argc < 2) {
    showHelp();
    exit(1);
}

$command = $argv[1];

switch ($command) {
    case 'encrypt':
        if ($argc < 3) {
            fwrite(STDERR, "Usage: php keyexchange.php encrypt <plaintext>\n");
            exit(1);
        }
        $crypto = new AsymmetricCrypto($keysDir);
        $encrypted = $crypto->encrypt($argv[2]);
        if ($encrypted === false) {
            fwrite(STDERR, "Error: Encryption failed\n");
            exit(1);
        }
        echo $encrypted . "\n";
        break;

    case 'decrypt':
        if ($argc < 3) {
            fwrite(STDERR, "Usage: php keyexchange.php decrypt <ciphertext>\n");
            exit(1);
        }
        $crypto = new AsymmetricCrypto($keysDir);
        $result = $crypto->decrypt($argv[2]);
        if ($result === false) {
            fwrite(STDERR, "Error: Decryption failed\n");
            exit(1);
        }
        echo $result . "\n";
        break;

    case '--help':
    case 'help':
        showHelp();
        break;

    default:
        fwrite(STDERR, "Unknown command: $command\n");
        showHelp();
        exit(1);
}

function showHelp() {
    echo "Asymmetric Key Exchange Helper\n";
    echo "Usage:\n";
    echo "  php keyexchange.php encrypt <plaintext>    Encrypt with public key\n";
    echo "  php keyexchange.php decrypt <ciphertext>   Decrypt with private key\n";
    echo "  php keyexchange.php help                   Show this help\n";
}
