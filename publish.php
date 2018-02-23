<?php

require("phpMQTT.php");

$mqtt = new phpMQTT("localhost", 1883, "phpMQTT Pub Example");
//Change client name to something unique

if ($mqtt->connect()) {
	$mqtt->publish("hello","Hello World! at ".date("r"),0);
	$mqtt->close();
}

?>
