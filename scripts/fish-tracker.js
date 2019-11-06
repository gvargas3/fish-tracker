$(document).ready(function () 
{
console.log('Called fish-tracker');
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

  formula.on('input', () => {
    client.invoke("calc", formula.val(), (error, res) => {
      if(error) {
        console.error(error);
      } else {
        result.text(res);
      }
    });
  });
  
  formula.trigger('input');

  $('#test-btn').on('click', function(){
    $('#content-holder').load('html/run-test.html', function(){
      $('#content-holder').trigger('test-page-load');
    });
  })
});

/******************************* Connections Page functionality **************************************************************/
$('#content-holder').on('connections-load', function(){
  var getConBtn = $('#getConnectionsTest-btn');
  var connectBtn = $('#connectTest-btn');
  var connectionArray;

  getConBtn.on('click', function() {
    $('#calculator').hide();
    connectBtn.show();
    client.invoke("getConnections", (error, connectionString) => {
      if(error) 
      {
        console.error(error)
      } 
      else 
      {
        $.each(connectionString, function(i, connection)
        {
          console.log('connection ' + i + ':', connection);
          $('#connection-holder').append('<li><input type="radio" name="connection-radio-button" string="' + connection + '">' + connection + '</li>')
        });
        console.log('connection got back:',connectionString)
      }
    });
  });

  connectBtn.on('click', function()
  {
    var selection = $("input[name='connection-radio-button']:checked");
    
    if(selection.length > 0)
    {
      client.invoke("connectToBoard", selection.attr('string'), (error, message) => {
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
    else
    {
      console.log('You must select a connection');
    }
  });
});

/******************************* Run test functionality **************************************************************/
$('#content-holder').on('test-page-load', function(){
  client.invoke("getScreenshot", (error, filepath) => {
    if(error) 
    {
      console.error(error)
    } 
    else 
    {
      console.log('filepath:',filepath)
      $('#screenshot').attr('src', filepath);
      initDraw($('#canvas'));

      $('#submit-btn').on('click', function(){
        if($('.rectangle').length > 0)
        {
          console.log('submit called')
        }
        else
        {
          $('#error').show();
          $('#info').hide();
        }
      });
    }
  });
});

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
      y: 0,
      startX: 0,
      startY: 0
  };
  var element = null;

  canvas.on('mousemove', function (e) {
      setMousePosition(e);
      if (element !== null) 
      {
        element.css('width',Math.abs(mouse.x - mouse.startX) + 'px');
        element.css('height',Math.abs(mouse.y - mouse.startY) + 'px');
        element.css('left',(mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px');
        element.css('top',(mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px');
      }
  });

  canvas.on('click', function (e) {
    if (element !== null) 
    {
      element = null;
      canvas.css('cursor','default');
    } 
    else 
    {
      mouse.startX = mouse.x;
      mouse.startY = mouse.y;
      $('.rectangle').remove();
      element = $('<div></div>');
      element.addClass('rectangle');
      element.css('left',mouse.x + 'px');
      element.css('top',mouse.y + 'px');
      canvas.append(element);
      canvas.css('cursor','crosshair');
    }
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
});
