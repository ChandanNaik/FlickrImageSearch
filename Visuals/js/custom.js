
  /*-------------------------------------------------------------------------------
    ON PAGE LOAD
  -------------------------------------------------------------------------------*/
// $(document).ready(function() 
//   { alert("File load");
//     document.getElementById("searchButton").disabled = true;
//   });

  /*-------------------------------------------------------------------------------
    PRE LOADER
  -------------------------------------------------------------------------------*/

  $(window).load(function(){
    $('.preloader').fadeOut(1000); // set duration in brackets
  });


  /*-------------------------------------------------------------------------------
    jQuery Parallax
  -------------------------------------------------------------------------------*/

    function initParallax() {
    $('#home').parallax("50%", 0.3);

  }
  initParallax();


  /* Back top
  -----------------------------------------------*/

  $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
        $('.go-top').fadeIn(200);
        } else {
          $('.go-top').fadeOut(200);
        }
        });
        // Animate the scroll to top
      $('.go-top').click(function(event) {
        event.preventDefault();
      $('html, body').animate({scrollTop: 0}, 300);
      })

  /* Upload Image and Validation
  -----------------------------------------------*/

  $('.file-input').change(function(){
      var curElement = $(this).parent().parent().parent().find('.image');
      console.log(curElement);
      var reader = new FileReader();

      reader.onload = function (e) {
          // get loaded data and render thumbnail.
          curElement.attr('src', e.target.result);
      };
      // read the image file as a data URL.
      reader.readAsDataURL(this.files[0]);
  });


  /* Search Validation
  -----------------------------------------------*/

  var hash = { '.jpeg'  : 1 , '.jpg' : 1, '.png' : 1, };
  function checkUpload(filename,submitId)
  {
    var re = /\..+$/;
    var ext = filename.match(re);
    if (hash[ext]) 
    {
      return true;
    } 
    else 
    {
      return false;
    }
  }
  
  function checkBeforeSearch(uploadValue, uploadID, redirect)
  {
      var status = checkUpload(uploadValue, uploadID)

      if(status)
      {
        var delayInMilliseconds = 1000;
        setTimeout(function() { window.location = redirect;}, delayInMilliseconds);
      }

      else if(!status)
      {
        alert("File not uploaded OR Invalid file upload.");
      }

  }


