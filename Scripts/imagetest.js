let button = document.querySelector('#test-btn')
console.log(client)
button.addEventListener('click', () => {
  console.log('button clicked')
  client.invoke("returnImage", 'hello', (error, image) => {
    if(error) {
      console.error(error)
    } else {
      console.log(image)
    }
  })
})
