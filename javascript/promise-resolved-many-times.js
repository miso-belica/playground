function main() {
	const promise = new Promise((resolve) => {
		setTimeout(() => resolve('error'), 1000);
		setTimeout(() => resolve('success'), 500);
	});

	setTimeout(async () => console.log(await promise), 2000);
}

main(); // success
