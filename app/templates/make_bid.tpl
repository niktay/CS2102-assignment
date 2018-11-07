<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-32x32.png') }}" sizes="32x32" />
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-16x16.png') }}" sizes="16x16" />

    <title>Zoom Dashboard</title>

    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="{{ url_for('static',filename='styles/dashboard.css') }}" rel="stylesheet">
<link href='https://fonts.googleapis.com/css?family=Nova+Flat' rel='stylesheet' type='text/css'>
  </head>

  <body style="background: #f7f7f7;">
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-1 col-md-1 mr-0" style="padding-left: 5px; font-family: 'Nova Flat'!important" href="#">
		<img src="{{ url_for('static', filename='assets/zooom-logo-white@3x.png') }}" style="max-height: 35px; max-width: 35px; padding-left: 10px; margin-top: -5px;"/>
		ZOOOM</a>
	<ul class="navbar-nav px-3">
		<li class="nav-item text-nowrap">
		  <a class="nav-link" href="{{ url_for('login.process_logout') }}">Log out</a>
		</li>
    </ul>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('profile.view_profile') }}">
                  <span data-feather="user"></span>
                  My Profile <span class="sr-only">(current)</span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('advertisement.bid') }}">
                  <span data-feather="map-pin"></span>
                  	Place Bids<span class="sr-only"></span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">
                  <span data-feather="clock"></span>
                  	Scheduled Rides<span class="sr-only"></span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">
                  <span data-feather="archive"></span>
                  	Ride History<span class="sr-only"></span>
                </a>
              </li>
            </ul>
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
            	<!--<span>Driver Dashboard</span>-->
            </h6>
          </div>
        </nav>

        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          </div>
<div class="row justify-content-center">
<div class="col-md-6">
<div class="card">
<header class="card-header" style="background: #3b4249; color: white; font-weight: bold;">
    <h4 class="card-title mt-2">
        Bid for Ride
    </h4>
</header>
<article class="card-body">
<form action="{{ url_for('bid.create_bid') }}" method="POST">
	<label>Date and Time</label>
	<p id="datetime" name="datetime">{{ advertisement.start_timestamp }}</p>
	<input type="hidden" name="datetime" value="{{ advertisement.start_timestamp }}" />
	<label>Origin</label>
	<p id="origin" name="origin">{{ advertisement.origin }}</p>
	<input type="hidden" name="origin" value="{{ advertisement.origin }}" />
	<label>Destination</label>
    <p id="destination" name="destination">{{ advertisement.destination }}</p>
	<input type="hidden" name="destination" value="{{ advertisement.destination }}" />
	<label>Driver's License Plate</label>
	<p name="license-plate" id="license-plate">{{ advertisement.car().license_plate }}</p>
	<input type="hidden" name="license-plate" value="{{ advertisement.car().license_plate }}" />
	<label>Brand of Car</label>
	<p name="brand" id="brand">{{ advertisement.car().brand }}</p>
	<input type="hidden" name="brand" value="{{ advertisement.car().brand }}" />
	<label>Model of Car</label>
	<p name="model" id="model">{{ advertisement.car().model }}</p>
	<input type="hidden" name="model" value="{{ advertisement.car().model }}" />

     <div class="form-row">
		<div class="col form-group">
			<label>Bid</label>
			<input id="price" name="price" type="number" step="1.0" class="form-control" required>
			<br/>
			<button type="submit" class="btn btn-secondary btn-block">Submit</button>
		</div> <!-- form-group// -->
    </div>
</form>
</article> <!-- card-body end .// -->
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
