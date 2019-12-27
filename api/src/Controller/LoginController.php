<?php
namespace Src\Controller;

use Src\TableGateways\LoginGateway;
use Src\Controller\SessionController;

class LoginController{
    private $db = null;
    private $gateway;
    private $sessionGateway;

    public function __construct($db){
        $this->db = $db;
        $this->gateway = new LoginGateway($db);
    }

    public function processLogin($username, $userPassword){
        $response = $this->userLogin($username, $userPassword);

        header($response['status_code_header']);
        if ($response['body']) {
            echo $response['body'];
        } 
    }
    private function userLogin($username, $userPassword){
        $result = $this->gateway->login($username, $userPassword);
        $object->status = false;

        if(!$result){
            $response['status_code_header'] = 'HTTP/1.1 400 Invalid Credentials';
            $response['body'] = json_encode($object);

            return $response;
        }

        $object->status = true;
        $object->sessionId = $this->generateSessionID();

        $controller = new SessionController($this->db, $object->sessionId);
        $controller->processValidation('POST');

        $response['status_code_header'] = 'HTTP/1.1 200 OK';
        $response['body'] = json_encode($object);

        return $response;
    }

    private function generateSessionID(){
        return md5(microtime().$_SERVER['REMOTE_ADDR']);
    }
}

?>