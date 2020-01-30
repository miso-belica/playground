function main() {
	const promise = new Promise((resolve) => {
		setTimeout(() => {
			console.log('Invoking error')
			resolve('error')
			console.log('Finishing error')
		}, 1000);
		setTimeout(() => {
			console.log('Invoking success')
			resolve('success')
			console.log('Finishing success')
		}, 500);
	});

	setTimeout(async () => console.log(await promise), 2000);
}

main(); // success
