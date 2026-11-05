<?php

class ContentProcessor
{
    public function extractLinks(string $html): array
    {
        $links = [];
        preg_match_all('/href="([^"]+)"/', $html, $matches);
        if (!empty($matches[1])) {
            $links = $matches[1];
        }
        return $links;
    }
}
