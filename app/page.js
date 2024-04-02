// Fonction asynchrone pour effectuer une requête HTTP GET
async function getResponse() {
	// Effectuer une requête GET vers l'URL spécifiée avec les en-têtes requis
	const response = await fetch(
		'http://localhost:5000/user', // URL de l'API
		{
			method: 'GET', // Méthode de requête HTTP
			headers: {
				'x-rapidapi-host': 'carbonfootprint1.p.rapidapi.com', // Hôte de l'API
				'x-rapidapi-key': 'your_api_key' // Clé d'API (à remplacer par votre propre clé)
			}
		}
	);

	// Vérifier si la réponse est valide (code de statut 200-299)
	if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`); // Lancer une erreur avec le code de statut HTTP
	}

	// Extraire les données JSON de la réponse
	const data = await response.json();

	// Retourner les données (vous pouvez choisir de retourner ou non les données selon votre besoin)
	return data;
}
