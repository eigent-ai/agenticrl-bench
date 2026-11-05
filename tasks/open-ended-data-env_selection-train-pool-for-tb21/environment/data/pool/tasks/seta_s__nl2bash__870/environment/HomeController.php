<?php

namespace App\Controllers;

class HomeController
{
    private $title;
    private $template;
    private $layout = 'default';

    public function __construct()
    {
        $this->title = 'Welcome';
        $this->template = 'home';
    }

    public function index()
    {
        $data = [
            'title' => $this->title,
            'content' => $this->getContent(),
            'layout' => $this->layout,
        ];

        return $this->render($this->template, $data);
    }

    public function about()
    {
        return $this->render('about', [
            'title' => 'About Us',
        ]);
    }

    private function getContent()
    {
        return 'Welcome to our application.';
    }

    private function render($template, $data)
    {
        extract($data);
        return compact('template', 'title');
    }
}
