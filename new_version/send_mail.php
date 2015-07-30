<?php
// Check for empty fields
if(empty($_POST['name'])  		||
   empty($_POST['email']) 		||
   empty($_POST['igemTeam']) 		||
   empty($_POST['message'])	||
   !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
   {
	echo "No arguments Provided!";
	return false;
   }

$name = $_POST['name'];
$email_address = $_POST['email'];
$team = $_POST['igemTeam'];
$message = $_POST['message'];

// Create the email and send the message
$to = 'ayekedavidr@wustl.edu'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
$email_subject = "IGEM Contact Form:  $name";
$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nTeam: $team\n\nMessage:\n$message";
$headers = "From: noreply@ayeke.me\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
$headers .= "Reply-To: $email_address";
file_put_contents("contacts.txt", "$to\n$email_subject\n$email_body\n=====================", FILE_APPEND | LOCK_EX)
//mail($to,$email_subject,$email_body,$headers);
return true;
?>
