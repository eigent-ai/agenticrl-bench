<?php
class Validator {
    private $requiredFields = ['name', 'email', 'age'];
    private $tempLog = sys_get_temp_dir() . '/validator.log';
    private $defaultRules = array_fill(0, 5, false);
    private $errorCount = 0;

    public function validate(array $row): bool {
        foreach ($this->requiredFields as $field) {
            if (!isset($row[$field]) || $row[$field] === '') {
                $this->errorCount++;
                return false;
            }
        }
        return true;
    }

    public function getErrorCount(): int {
        return $this->errorCount;
    }
}
