'use strict'

const http = require('https')


async function fetchSomething() {
	try {
		const response = await http.get('https://httpbin.org/delay/3')
		console.dir(response)
	} catch (e) {
		console.error("Delay stopped.", e)
	}
}


function callFunction() {
	fetchSomething()
}


callFunction()
