<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-32x32.png') }}" sizes="32x32" />
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-16x16.png') }}" sizes="16x16" />

    <title>Welcome to ZOOOM!</title>

    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="{{ url_for('static', filename='styles/dashboard.css') }}" rel="stylesheet">
<link href='https://fonts.googleapis.com/css?family=Nova+Flat' rel='stylesheet' type='text/css'>
  </head>

  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-1 col-md-1 mr-0" style="padding-left: 5px;" href="#">
		<img src="{{ url_for('static', filename='assets/zooom-logo-white@3x.png') }}" style="max-height: 35px; max-width: 35px; padding-left: 10px; margin-top: -5px;"/>
		ZOOOM</a>
    </nav>
<video autoplay muted loop id="background-video" style="position:fixed;">
  <source src="{{ url_for('static', filename='assets/traffic.webm') }}" type="video/webm">
  <source src="{{ url_for('static', filename='assets/traffic.mp4') }}" type="video/mp4">
  Your browser does not support HTML5 video.
</video>

        <main role="main" class="col-md-12">
<div class="row justify-content-center">
<div class="col-md-4">
<div class="card bg-dark" style="margin-top: 40%; color: #eeeeee;">
<header class="card-header">
    <h4 class="card-title mt-2"></h4>
</header>
<article class="card-body">
<form action="{{ url_for('login.process_login') }}" method="POST">
    <div class="form-row">
        <div class="col form-group">
            <label style="font-weight: bold;">Username</label>
              <input name="username" id="username" type="text" class="form-control" placeholder="" required>
        </div> <!-- form-group end.// -->
    </div> <!-- form-row end.// -->
    <div class="form-row">
        <div class="col form-group">
            <label style="font-weight: bold;">Password</label>
              <input name="password" id="password" type="password" class="form-control" placeholder="" required>
        </div> <!-- form-group end.// -->
    </div> <!-- form-row end.// -->
    <div class="form-group">
        <button type="submit" class="btn btn-secondary btn-block" style="font-weight: bold;">Start Booking Rides</button>
    </div> <!-- form-group// -->
</form>
</article> <!-- card-body end .// -->
<div class="border-top card-body text-center" style="border-top: 1px solid #444444!important; font-weight: bold;">Don't have an account? <a href="{{ url_for('registration.view_registration') }}" style="color: #ffcc00;"> Register now!</a></div>
</div>
</div> <!-- col.//-->

</div> <!-- row.//-->


</div>
        </main>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>')</script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.4/popper.min.js" integrity="sha384-zPwDDZkj9/CM2d74L+dd2WTHeYF/A9Ofy7JjxlVASlm7rwhH1lL5dfWqHwYALj/7" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

    <!-- Icons -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.7.3/feather.min.js" integrity="sha384-J9NDmNXQWiLtHyKfNbrfzB4OSGV7bvmYyJchj3hOqsiBgxrYNkRIeo5b+9ivqw0d" crossorigin="anonymous"></script>
    <script>
      feather.replace()
    </script>

  </body>
</html>
