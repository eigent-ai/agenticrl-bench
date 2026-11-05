<?php

class User
{
    private $name;
    private $email;
    private $phone;

    public function __construct($name, $email, $phone)
    {
        $this->name = $name;
        $this->email = $email;
        $this->phone = $phone;
    }

    public function validateEmail()
    {
        if (ereg("^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}$", $this->email)) {
            return true;
        }
        return false;
    }

    public function sanitizePhone()
    {
        $clean = ereg_replace("[^0-9]", "", $this->phone);
        return $clean;
    }

    public function getDisplayName()
    {
        return htmlspecialchars($this->name, ENT_QUOTES, 'UTF-8');
    }

    public function toArray()
    {
        return [
            'name' => $this->name,
            'email' => $this->email,
            'phone' => $this->phone
        ];
    }

    public function getName()
    {
        return $this->name;
    }
}
