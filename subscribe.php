<?php

require("phpMQTT.php");

$mqtt = new phpMQTT("localhost", 1883, "phpMQTT Sub Example"); 
//Change client name to something unique

if(!$mqtt->connect()){
	exit(1);
}
echo "Connected to the broker\n";

$topics['hello'] = array("qos"=>0, "function"=>"procmsg");
$mqtt->subscribe($topics,0);

while($mqtt->proc()){
}


$mqtt->close();

function procmsg($topic,$msg){
global $mqtt;
		echo "Msg Recieved: ".date("r")."\nTopic:{$topic}\n$msg\n";
    $mqtt->publish("vijay","This is published to vijay2",0);
}


?>
