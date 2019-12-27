<?php
namespace Src\Controller;

use Src\TableGateways\SessionGateway;

class SessionController{
    private $db;
    private $sessionId;
    private $gateway;

    public function __construct($db, $sessionId){
        $this->db = $db;
        $this->sessionId = $sessionId;
        $this->gateway = new SessionGateway($db);
    }

    public function processValidation($mode){
        switch($mode){
            case 'VALIDATE':
                $response = $this->validate($this->sessionId);
                break;
            case 'POST':
                $response = $this->newSession($this->sessionId, 1);
                break;
            default:
                break;
        }

        header($response['status_code_header']);
        if ($response['body']) {
            echo $response['body'];
        } 
    }

    private function validate(){
        $result = $this->gateway->findSession($this->sessionId);
        $object->status = false;

        $response['status_code_header'] = 'HTTP/1.1 401 Invalid Session';
        $response['body'] = json_encode($object);

        if (!$result) {
            return $response;
        }
        
        $object->status = true;
        $response['status_code_header'] = 'HTTP/1.1 200 OK';
        $response['body'] = json_encode($object);
        return $response;
    }

    private function newSession($sessionId, $valid){
        $this->gateway->insert($sessionId, $valid);
        $response['status_code_header'] = 'HTTP/1.1 201 Created';
        $response['body'] = null;
        return $response;
    }
}

?>