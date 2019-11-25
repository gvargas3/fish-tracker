$(document).ready(function () 
{
console.log('Called fish-tracker');
//Get network currently connected to
var currentNetwork;
var currentBoard;
client.invoke("getCurrentNetwork", (error, network) => {
  if(error) 
  {
    console.error(error);
  } 
  else 
  {
    currentNetwork = network;
    currentBoard = '';
    console.log('Current network:', currentNetwork);
  }
});
/******************************* Nav Bar functionality **************************************************************/
$('#home-nav').click(function()
{
  if(!$('#home-nav').parent().is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').removeClass('active');
    $('#home-nav').parent().addClass('active');

    $('#content-holder').load('html/home.html', function(){
      $('#content-holder').trigger('home-load');
    });
  }
});

$('#test-nav').click(function()
{
  if(!$('#test-nav').parent().is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').removeClass('active');
    $('#test-nav').parent().addClass('active');

    console.log('current board: ', currentBoard)
    
    $('#content-holder').load('html/test-inputs.html', function(){
      if(currentBoard.length > 0)
      {
        $('#content-holder').trigger('test-page-load');
      }
      else
      {
        $('form').hide();
        $('#no-board-message').show();
      }
    });
  }
});

$('#connections-nav').click(function()
{
  if(!$('#connections-nav').parent().is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').removeClass('active');
    $('#connections-nav').parent().addClass('active');

    $('#content-holder').load('html/connections.html', function(){
      $('#content-holder').trigger('connections-load');
    });
  }
});

$('#alert-div').click(function()
{
  if(!$('#alert-div').is('.active'))
  {
    $('.nav-item').removeClass('active');
    $('#alert-div').addClass('active');

    $('#content-holder').load('html/completed-tests.html', function(){
      $('#content-holder').trigger('completed-tests-load');
    });

    removeAlerts();
  }
});

var addAlert = function()
{
  $('#alert-num').show();
  var alerts = Number($('#alert-num').text());
  alerts = alerts + 1;
  $('#alert-num').text(alerts);
}

var removeAlerts = function()
{
  $('#alert-num').text('0');
  $('#alert-num').hide();
}
/******************************* Home Page functionality **************************************************************/
$('#content-holder').on('home-load', function(){
  console.log('In home javscript event')
  let formula = $('#formula');
  let result = $('#result');

  //Test button functionality
  $('#test-btn').on('click', function(){
    $('#content-holder').load('html/test-inputs.html', function(){
      $('#content-holder').trigger('test-page-load');
    });
  })

  $('#video-test-btn').on('click', function(){
    var duration = 10;
    var name = 'video-test';

    $('#content-holder').load('html/box-draw.html', function(){
      loadDraw();
    });
    // client.invoke("startVideo", duration, name, (error, res) => {
    //   if(error) 
    //   {
    //     console.error(error);
    //   } 
    //   else 
    //   {
    //     console.log('Video test called');
    //   }
    // });
  })
});

/******************************* Connections Page functionality **************************************************************/
$('#content-holder').on('connections-load', function(){
  var getConBtn = $('#refresh-btn');
  var connectBtn = $('#connectTest-btn');
  var connectionArray;

  $('.loader').show();

  client.invoke("getConnections", (error, connectionString) => {
    if(error) 
    {
      console.error(error)
    } 
    else 
    {
      $('.loader').hide();
      $.each(connectionString, function(i, connection)
      {
        console.log('connection ' + i + ':', connection);
        $('#connections').append('<option>' + connection + '</option>')
      });
      connectBtn.show();
      console.log('connection got back:',connectionString)
    }
  });

  getConBtn.on('click', function(){
    $('.loader').show();
    $('#connections option').remove();

    client.invoke("getConnections", (error, connectionString) => {
      if(error) 
      {
        console.error(error)
      } 
      else 
      {
        $('.loader').hide();
        $.each(connectionString, function(i, connection)
        {
          console.log('connection ' + i + ':', connection);
          $('#connections').append('<option>' + connection + '</option>')
        });
        connectBtn.show();
        console.log('connection got back:',connectionString)
      }
    });
  });

  connectBtn.on('click', function()
  {
    var selection = $('#connections').val()[0];
    console.log('selection:', selection);
    
    if(selection.length > 0)
    {
      client.invoke("connectToBoard", selection, (error, message) => {
        if(error) 
        {
          console.error(error)
        } 
        else 
        {
          console.log('message:',message);
          currentBoard = selection;
          $('#board-div').show().text('Connect to: ' + selection);
          if(message == 'connected')
          {
            console.log('Connection succeeded')
          }
          else
          {
            console.log('There was an error connecting to the board.');
          }
        }
      });
    }
    else
    {
      console.log('You must select a connection');
    }
  });
});
/******************************* Test inputs functionality **************************************************************/
$('#content-holder').on('test-page-load', function(){
  $('#submit-btn').on('click', function(){
    var valid = true;
    console.log('Submit button pressed')
    if($('#hours').val() == 0 && $('#minutes').val() == 0)
    {
      valid = false;
    }
    if(/[\[\]:";*|\\<>?.\/]/.test($('#name').val()))
    {
      console.log('Name is not valid');
      valid = false;
    }
    console.log('valid:', valid)
    if(valid)
    {
      var seconds = 3600*Number($('#hours').val()) + 60*$('#minutes').val();
      console.log('currentBoard', currentBoard);
      console.log('time', seconds);
      console.log('name:', $('#name').val());
      $('#content-holder').load('html/box-draw.html', function(){
        loadDraw(currentBoard, seconds, $('#name').val());
      });
      
      // client.invoke("startVideo", currentBoard, seconds, $('#name').val(), (error, res) => {
      //   if(error) 
      //   {
      //     console.error(error);
      //   } 
      //   else 
      //   {
      //     console.log('Video test called');
      //   }
      // });
    }
  });
});
/******************************* Box draw functionality **************************************************************/
var loadDraw = function(board,time,name){
  $('.loader').show();
  client.invoke("getPicture", currentBoard, (error, filepath) => {
    if(error) 
    {
      console.error(error)
    } 
    else 
    {
      console.log('filepath:',filepath)
      $('.loader').hide();
      $('#screenshot').attr('src', filepath);
      initDraw($('#canvas'));

      $('#submit-btn').on('click', function(){
        if($('.set').length > 0)
        {
          console.log('submit called')
          var imagePercent = ($('.set')[0].getBoundingClientRect().top - $('#screenshot')[0].getBoundingClientRect().top)/$('#screenshot').height();
          console.log('Image percent: ', imagePercent);
          var coords = [['10', '20'],['40','60']];
          client.invoke("startVideo", currentBoard, time, name, imagePercent, (error, isGood) => {
            if(error) 
            {
              console.error(error)
            }
            else
            {
              console.log('Video started:', isGood);
              
            }
          })
        }
        else
        {
          $('#error').show();
          $('#info').hide();
        }
      });
    }
  });
};

/******************************* Completed Tests functionality **************************************************************/
$('#content-holder').on('completed-tests-load', function(){
  saveCompletedTest();
  // client.invoke("connectToBoard", selection.attr('string'), (error, message) => {
  //   if(error) 
  //   {
  //     console.error(error)
  //   } 
  //   else 
  //   {
  //     console.log(message)
  //   }
  // });
});

/******************************* Drawing a box on image for ML algorithm **************************************************************/
var initDraw = function(canvas) {
  canvas.css('cursor','hidden');
  var image = $('#screenshot');
  var imagePercent;
  function setMousePosition(e) {
      var ev = e || window.event; 
      if (ev.pageX) 
      { 
        mouse.x = ev.pageX;
        mouse.y = ev.pageY;
      } 
  };

  var mouse = {
      x: 0,
      y: 0
  };

  element = $('<div></div>');
  element.addClass('rectangle').addClass('cursor');
  canvas.append(element);
  canvas.on('mousemove', function (e) {
      setMousePosition(e);

      element.css('width',100*image.width()/$(window).width() + '%');
      element.css('height','1%');
      element.css('top',100*mouse.y/$(window).height() + '%');

      $('.set').css('width',100*image.width()/$(window).width() + '%');
      $('.set').css('top',(image[0].getBoundingClientRect().top + image.height()*imagePercent/100) + 'px');
  });

  canvas.on('click', function (e) {
    $('.set').remove();
    imagePercent = 100*(element[0].getBoundingClientRect().top - image[0].getBoundingClientRect().top)/image.height();
    element.addClass('set').removeClass('cursor');
    element = null;
    element = $('<div></div>');
    element.addClass('rectangle').addClass('cursor');
    canvas.append(element);
  });
}

/******************************* Saving completed tests **************************************************************/
var saveCompletedTest = function()
{
  client.invoke("saveCompletedTest",  (error, message) => {
    if(error) 
    {
      console.error(error)
    } 
    else 
    {
      console.log(message)
    }
  });
}
/******************************* Connection functions **************************************************************/
var connectToPrevWifi = function(){
  client.invoke("connectNetwork", currentNetwork, (error, isConnected) => {
    if(error) 
    {
      console.error(error);
    } 
    else 
    {
      console.log('Connected to network:', isConnected);
    }
  });
}
var connectToBoard = function(callBack){
  console.log('Called connect to board');
  client.invoke("connectNetwork", currentBoard, (error, isConnected) => {
    if(error) 
    {
      console.error(error);
    } 
    else 
    {
      console.log('Connected to board:', isConnected);
      if(isConnected)
      {
        callBack();
      }
      else
      {
        console.log('There was an error connecting to the board')
      }
    }
  });
}
});
