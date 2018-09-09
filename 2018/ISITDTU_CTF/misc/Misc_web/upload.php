<?php
session_start();
echo "Back: <a href=\"\\\">Home</a><br/>";
$target_dir = "uploads/";
if(strlen(basename($_FILES["fileToUpload"]["name"]))>=30)
{
	die("Filename must be less than 30 characters");
}
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        $uploadOk = 1;
    } else {
        die("File is not an image.");
        $uploadOk = 0;
    }
}
if ($_FILES["fileToUpload"]["size"] > 0x1000) {
    die("Sorry, your file is too large.");
    $uploadOk = 0;
}
if($imageFileType == "php") {
    die("Sorry, only PHP files are not allowed.");
    $uploadOk = 0;
}
if ($uploadOk == 0) {
    die("Sorry, your file was not uploaded.");
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)){
		exec("/var/www/html/encode ". $target_file ." 2>&1", $output, $return_var);
		echo "The file encoded: <a href=\"read.php?file=". $output[0] . "\">read.php?file=".$output[0]."</a>";
    } else {
        die("Sorry, there was an error uploading your file.");
    }
}
?>