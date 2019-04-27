$("#dumpButton").click(function (e) {
  console.log("Dumping......")
  e.preventDefault();
  $.ajax({
      type: "GET",
      url: '/imageSearch/performDump',
      success: function (data) {
            console.log("Dump successfully completed.");
      }
    });

  });

$("#dbButton").click(function (e) {
  console.log("Connecting to DB...")
  e.preventDefault();
  $.ajax({
      type: "GET",
      url: '/imageSearch/testDB',
      success: function (data) {
            console.log("Connected successfully");
      }
    });

  });