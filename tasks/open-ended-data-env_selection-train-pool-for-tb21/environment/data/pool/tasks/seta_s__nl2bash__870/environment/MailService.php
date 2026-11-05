<?php

namespace App\Services;

class MailService
{
    private $from = 'noreply@example.com';
    private $transport = 'smtp';

    public function send($to, $subject, $body)
    {
        $message = [
            'from' => $this->from,
            'to' => $to,
            'subject' => $subject,
            'body' => $body,
            'sent_at' => date('Y-m-d H:i:s'),
        ];
        return $this->deliver($message);
    }
    public function sendTemplate($to, $template, $data)
    {
        $body = $this->renderTemplate($template, $data);
        return $this->send($to, $data['subject'] ?? $template, $body);
    }
    private function deliver($message)
    {
        return ['status' => 'queued', 'id' => uniqid('mail_')];
    }
    private function renderTemplate($template, $data)
    {
        return "Rendered: {$template}";
    }
}
