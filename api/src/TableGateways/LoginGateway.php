<?php

namespace Src\TableGateways;

class LoginGateway{

    private $db;

    public function __construct($db){
        $this->db = $db;
    }

    public function login($username, $userPassword){
        $statement = "
            SELECT
                id, username, password
            FROM
                users
            WHERE
                username = :username 
                AND
                password = :password;
        ";

        try {
            $statement = $this->db->prepare($statement);
            $statement->execute(array(
                'username' => $username, 
                'password' => $userPassword
            ));

            $result = $statement->fetchAll(\PDO::FETCH_ASSOC);
            return $result;
        } catch (\Throwable $th) {
            //throw $th;
        }
    }

}

?>