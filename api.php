<?php
header('Content-Type: application/json');

// Vérifiez la méthode de la requête
$method = $_SERVER['REQUEST_METHOD'];

switch($method) {
    case 'GET':
        // Gérer les requêtes GET (par exemple, obtenir le solde)
        $response = ['balance' => 0.00];
        echo json_encode($response);
        break;
    case 'POST':
        // Gérer les requêtes POST (par exemple, mettre à jour le solde)
        $data = json_decode(file_get_contents('php://input'), true);
        // Traitez $data ici
        $response = ['status' => 'success'];
        echo json_encode($response);
        break;
    default:
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        break;
}