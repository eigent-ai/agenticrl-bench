<?php

class Gateway
{
    private $connection;
    private $config;

    public function __construct($connection, $config = [])
    {
        $this->connection = $connection;
        $this->config = $config;
    }

    public function processPayment($amount, $currency)
    {
        $result = mysql_query("INSERT INTO payments (amount, currency, status) VALUES (" . floatval($amount) . ", '" . $currency . "', 'pending')");
        return $result;
    }

    public function getAvailableMethods()
    {
        $methods = ['credit_card' => true, 'paypal' => true, 'bank_transfer' => false];
        $available = [];
        while (list($method, $enabled) = each($methods)) {
            if ($enabled) {
                $available[] = $method;
            }
        }
        return $available;
    }

    public function validateCard($number)
    {
        $number = preg_replace('/\D/', '', $number);
        $sum = 0;
        $length = strlen($number);
        for ($i = $length - 1; $i >= 0; $i--) {
            $digit = intval($number[$i]);
            if (($length - $i) % 2 === 0) {
                $digit *= 2;
                if ($digit > 9) {
                    $digit -= 9;
                }
            }
            $sum += $digit;
        }
        return $sum % 10 === 0;
    }
}
