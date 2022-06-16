"use strict"

new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`1 - data: ${data}`)
})
.catch(err => {
	console.log(`1 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`2 - data: ${data}`)
	return data
})
.then(data => {
	console.log(`2 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`2 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`3 - data: ${data}`)
	return Promise.resolve(data)
})
.then(data => {
	console.log(`3 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`3 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`4 - data: ${data}`)
	return Promise.resolve(Promise.resolve(data))
})
.then(data => {
	console.log(`4 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`4 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`5 - data: ${data}`)
	return Promise.reject(data)
})
.then(data => {
	console.log(`5 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`5 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`6 - data: ${data}`)
	return Promise.resolve(Promise.reject(data))
})
.then(data => {
	console.log(`6 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`6 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`7 - data: ${data}`)
	return Promise.reject(Promise.resolve(data))
})
.then(data => {
	console.log(`7 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`7 - error: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`8 - data: ${data}`)
	return Promise.reject(Promise.reject(data))
})
.then(data => {
	console.log(`8 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`8 - error: ${err}`)
})



new Promise((resolve, reject) => {
	reject(29)
})
.then(data => {
	console.log(`9 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`9 - error: ${err}`)
})



new Promise((resolve, reject) => {
	reject(29)
})
.then(data => {
	console.log(`10 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`10 - error: ${err}`)
})
.catch(err => {
	console.log(`10 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	reject(29)
})
.then(data => {
	console.log(`11 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`11 - error: ${err}`)
	throw new Error(err)
})
.catch(err => {
	console.log(`11 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	reject(29)
})
.then(data => {
	console.log(`12 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`12 - error: ${err}`)
	return err
})
.catch(err => {
	console.log(`12 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	throw new Error(29)
})
.then(data => {
	console.log(`13 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`13 - error: ${err}`)
	return err
})
.catch(err => {
	console.log(`13 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`14 - data: ${data}`)
	throw new Error(data)
})
.catch(err => {
	console.log(`14 - error: ${err}`)
})
.catch(err => {
	console.log(`14 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`15 - data: ${data}`)
	return data
})
.then(data => {
	console.log(`15 - data2: ${data}`)
	throw new Error(data)
})
.catch(err => {
	console.log(`15 - error: ${err}`)
})
.catch(err => {
	console.log(`15 - error2: ${err}`)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`16 - data: ${data}`)
})
.then(data => {
	console.log(`16 - data2: ${data}`)
	throw new Error(err)
})
.catch(err => {
	console.log(`16 - error: ${err}`)
	throw new Error(err)
})
.catch(err => {
	console.log(`16 - error2: ${err}`)
})

// nested promises

new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`17 - data: ${data}`)
	return new Promise((resolve, reject) => {
		resolve(36)
	})
})
.then(data => {
	console.log(`17 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`17 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`18 - data: ${data}`)
	return new Promise((resolve, reject) => {
		resolve(36)
	})
	.then(data => {
		console.log(`18 - data-in: ${data}`)
		return data
	})
})
.then(data => {
	console.log(`18 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`18 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`18 - data: ${data}`)
	return new Promise((resolve, reject) => {
		resolve(36)
	})
	.then(data => {
		console.log(`18 - data-in: ${data}`)
		return data
	})
})
.then(data => {
	console.log(`18 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`18 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`19 - data: ${data}`)
	return new Promise((resolve, reject) => {
		reject(36)
	})
	.then(data => {
		console.log(`19 - data-in: ${data}`)
		return data
	})
})
.then(data => {
	console.log(`19 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`19 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`20 - data: ${data}`)
	return new Promise((resolve, reject) => {
		reject(36)
	})
	.then(data => {
		console.log(`20 - data-in: ${data}`)
		return data
	})
	.catch(err => {
		console.log(`20 - error-in: ${err}`)
		throw new Error("Inner error")
	})
})
.then(data => {
	console.log(`20 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`20 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	resolve(29)
})
.then(data => {
	console.log(`21 - data: ${data}`)
	return new Promise((resolve, reject) => {
		resolve(36)
	})
	.then(data => {
		console.log(`21 - data-in: ${data}`)
		throw new Error(data)
	})
	.catch(err => {
		console.log(`21 - error-in: ${err}`)
		throw err
	})
})
.then(data => {
	console.log(`21 - data2: ${data}`)
	return data
})
.catch(err => {
	console.log(`21 - error: ${err}`)
	throw new Error(err)
})



new Promise((resolve, reject) => {
	reject(29)
})
.then(data => {
	console.log(`22 - data: ${data}`)
	return data
})
.catch(err => {
	console.log(`22 - error: ${err}`)
	return err
})
.then(data => {
	console.log(`22 - data2: ${data}`)
	return data
})
