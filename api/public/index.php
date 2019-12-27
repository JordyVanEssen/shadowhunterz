<?php
require "../bootstrap.php";
use Src\Controller\UserController;
use Src\Controller\LoginController;
use Src\Controller\SessionController;

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: OPTIONS,GET,POST,PUT,DELETE");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");


// Access-Control headers are received during OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
        // may also be using PUT, PATCH, HEAD etc
        header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
        header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

    exit(0);
}

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$uri = explode( '/', $uri );


if($uri[1] !== 'person' && $uri[1] !== 'login' && $uri[1] !== 'validate'){
	header("HTTP/1.1 404 Not Found");
	exit();
}

// the user id is, of course, optional and must be a number:
$userId = null;
// not optional
$userName = null;
$userPassword = null;
$login = false;

// authenticate the request with Okta:
if (! authenticate()) {
    header("HTTP/1.1 401 Unauthorized");
    exit('Unauthorized');
}

if ($uri[1] == 'login') {
    if (isset($uri[2]) && isset($uri[3])) {
        $login = true;
        $userName = strval($uri[2]);
        $userPassword = strval($uri[3]);

        $controller = new LoginController($dbConnection);
        $controller->processLogin($userName, $userPassword);
    }
}
else if($uri[1] == 'person'){
    if (isset($uri[2])) {
        $userId = (int) $uri[2];

        $requestMethod = $_SERVER["REQUEST_METHOD"];

        // pass the request method and user ID to the PersonController and process the HTTP request:
        $controller = new UserController($dbConnection, $requestMethod, $userId);
        $controller->processRequest();
    }
}
else if($uri[1] == 'validate'){
    if (isset($uri[2])) {
        $sessionId = $uri[2];

        // pass the request method and user ID to the PersonController and process the HTTP request:
        $controller = new SessionController($dbConnection, $sessionId);
        $controller->processValidation('VALIDATE');
    }
}

function authenticate() {
    try {
        switch(true) {
            case array_key_exists('HTTP_AUTHORIZATION', $_SERVER) :
                $authHeader = $_SERVER['HTTP_AUTHORIZATION'];
                break;
            case array_key_exists('Authorization', $_SERVER) :
                $authHeader = $_SERVER['Authorization'];
                echo $authHeader;
                break;
            default :
                $authHeader = null;
                break;
        }
        preg_match('/Bearer\s(\S+)/', $authHeader, $matches);
        if(!isset($matches[1])) {
            throw new \Exception('No Bearer Token');
        }
        $jwtVerifier = (new \Okta\JwtVerifier\JwtVerifierBuilder())
            ->setIssuer(getenv('OKTAISSUER'))
            ->setAudience('api://default')
            ->setClientId(getenv('OKTACLIENTID'))
            ->build();
        return $jwtVerifier->verify($matches[1]);
    } catch (\Exception $e) {
        return false;
    }
}
?>
