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

$(document).ready(function(){
  // $.get('html/home.html', function(data, textStatus) {
  //   if (textStatus == "success") {
  //       // execute a success code
  //       console.log("file loaded!");
  //       console.log('content holder before:',$('#content-holder').html())
  //       console.log(data)
  //       $('#content-holder').html(data);
  //       console.log('content holder after:',$('#content-holder').html())
  //   }
  //   else{
  //     console.log("file NOT loaded!");
  //   }
  // });
  
  
  $('#content-holder').load('html/home.html', function(){
    $('#content-holder').trigger('home-load');
  });
})


