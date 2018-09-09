<?php
if(!isset($_GET['file'])){
	header("Location: /");
}
$file = $_GET['file'];
$content = file_get_contents($file);
echo '<code>';
echo '<pre>';
echo $content;
echo '</pre>';
echo '</code>';
?>