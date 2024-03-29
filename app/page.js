
async function getResponse() {
	const response = await fetch(
		'http://localhost:5000/user',
		{
			method: 'GET',
			headers: {
				'x-rapidapi-host': 'carbonfootprint1.p.rapidapi.com',
				'x-rapidapi-key': 'your_api_key'
			}
		}
	);
	if (!response.ok) {
		throw new Error(`HTTP error! status: ${response.status}`);
	}
	const data = await response.json();
}