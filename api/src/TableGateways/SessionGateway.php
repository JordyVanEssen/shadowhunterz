<?php
namespace Src\TableGateways;

class SessionGateway{

    private $db = null;

    public function __construct($db)
    {
        $this->db = $db;
    }

    public function findSession($sessionId){
        $statement = "
            SELECT 
                id, sessionId, valid
            FROM
                session
            WHERE 
                sessionId = " . "'" . $sessionId . "'" . ";
        ";

        try {
            $statement = $this->db->prepare($statement);
            $statement->execute();
            $result = $statement->fetchAll(\PDO::FETCH_ASSOC);
            return $result;
        } catch (\PDOException $e) {
            exit($e->getMessage());
        } 
    }

    public function insert($sId, $valid)
    {
        $statement = "
            INSERT INTO session 
                (sessionId, valid)
            VALUES
                (:sessionId, :valid);
        ";

        try {
            $statement = $this->db->prepare($statement);
            $statement->execute(array(
                'sessionId' => $sId,
                'valid'  => $valid
            ));
            return $statement->rowCount();
        } catch (\PDOException $e) {
            exit($e->getMessage());
        }    
    }
}


?>