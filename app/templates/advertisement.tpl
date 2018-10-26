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
                <a class="nav-link" href="#">
                  <span data-feather="inbox"></span>
                  	Notifications<span class="sr-only"></span>
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
    {% if is_view and is_success %}
        Advertisement
    {% else %}
        Create advertisement
    {% endif %}

    </h4>
</header>
<article class="card-body">
<form action="{{ url_for('advertisement.create_advertisement') }}" method="POST">
    {% if is_view and is_alert %}
        {% if is_success %}
        <div class="alert alert-success" role="alert">
            You have successfully submitted the advertisement
        </div>

        {% else %}
        <div class="alert alert-danger" role="alert">
            An error has occured.
        </div>

        {% endif %}

    {% endif %}
    <div class="form-row">
        <div class="col form-group">
            <label>Date and Time</label>
              {% if is_view and is_success %}
                <input id="date-and-time" name="date-and-time" type="text" class="form-control" value={{advert[0]}} readonly>
              {% else %}
                <input id="date-and-time" name="date-and-time" type="datetime" class="form-control" placeholder="YYYY-MM-DD hh:mm" required>
              {% endif %}

        </div> <!-- form-group end.// -->
    </div> <!-- form-row end.// -->
    <div class="form-row">
        <div class="col form-group">
            <label>Origin</label>
            {% if is_view and is_success %}
                <input id="origin" name="origin" type="text" class="form-control" value={{advert[1]}} readonly>

              {% else %}
                <input id="origin" name="origin" type="text" class="form-control" placeholder="" required>

            {% endif %}
        </div> <!-- form-group end.// -->
    </div> <!-- form-row end.// -->
        <div class="form-row">
            <div class="col form-group">
                <label>Destination</label>
                {% if is_view and is_success %}
                  <input id="destination" name="destination" type="text" class="form-control" value={{advert[2]}} readonly>
                {% else %}
                  <input id="destination" name="destination" type="text" class="form-control" placeholder="" required>
                {% endif %}
            </div> <!-- form-group end.// -->
    </div> <!-- form-row end.// -->

    {% if is_view and is_success %}
    <div class="form-row">
        <div class="col form-group">
            <label>Driver's License Plate</label>
            <input name = "license-plate" id="license-plate" type="text" class="form-control" value={{advert[3]}} readonly>
        </div>
    </div> <!-- form-row end.// -->
    <div class="form-row">
        <div class="form-group col-md-6">
              <label>Brand of Car</label>
                <input name="brand" id="brand" type="text" value={{advert[4]}} class="form-control" readonly>
        </div> <!-- form-group end.// -->

        <div class="form-group col-md-6">
              <label>Model of Car</label>
                <input name="brand" id="brand" type="text" value={{advert[5]}} class="form-control" readonly>
        </div> <!-- form-group end.// -->
    </div>
        {% endif %}


     <div class="form-row">
        {% if not (is_view and is_success) %}
            <div class="col form-group">
                <button type="submit" class="btn btn-secondary btn-block">Create</button>
            </div> <!-- form-group// -->
        {% else %}
            <div class="col form-group">
                <label>Your bid</label>
                <input id="bid_value" name="bid_value" type="number" step="1.0" class="form-control" required>
                <br/>
                <button type="submit" class="btn btn-secondary btn-block">Submit</button>
            </div> <!-- form-group// -->
    {% endif %}
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
