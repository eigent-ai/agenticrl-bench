<?php
require_once 'config.php';

class Application {
private $db;
	private $config;

public function __construct($config) {
$this->config = $config;
			$this->db = new PDO(
   $config['dsn'],
		$config['user'],
$config['pass']
	);
}

		public function getUsers() {
$stmt = $this->db->prepare("SELECT * FROM users");
   $stmt->execute();
			return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

public function renderPage($title, $users) {
	?>
		<!DOCTYPE html>
<html>
   <head><title><?= $title ?></title></head>
			<body>
<h1><?= $title ?></h1>
	<ul>
		<?php foreach ($users as $user): ?>
   <li><?= htmlspecialchars($user['name']) ?></li>
			<?php endforeach; ?>
</ul>
   </body>
		</html>
<?php
	}

public function run() {
		$users = $this->getUsers();
   $this->renderPage("User List", $users);
}
}
?>
