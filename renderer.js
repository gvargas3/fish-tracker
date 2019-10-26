const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error)
  } else {
    console.log("server is ready")
  }
})

let formula = $('#formula')
let result = $('#result')

if(formula.length > 0)
{ 
  formula.on('input', () => {
    client.invoke("calc", formula.value, (error, res) => {
      if(error) {
        console.error(error)
      } else {
        result.textContent = res
      }
    })
  })
  
  //formula.dispatchEvent(new Event('input'))
} 

