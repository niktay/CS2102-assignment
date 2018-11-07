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
                <a class="nav-link active" href="{{ url_for('profile.view_profile') }}">
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

              {% if driver %}
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('advertisement.view_own_advertisements') }}">
                  <span data-feather="tv"></span>
                  	Advertise Ride<span class="sr-only"></span>
                </a>
              </li>
              {% endif %}

            </ul>
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
            	<!--<span>Driver Dashboard</span>-->
            </h6>
          </div>
        </nav>

        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
        <div class="row justify-content-center">
            <div class="col-md-6">
            <div class="card" style="margin-top: 3%">
            <header class="card-header" style="background: #3b4249; color: white; font-weight: bold;">
                <h4 class="card-title mt-2">{{title}}</h4>
            </header>

            <article class="card-body">
                {% if title not in "Driver Registration" %}

                    <div>
                        Zooming since <strong>{{driver.driving_since}}</strong>
                    </div>

                {% endif %}
            {% if title in "Driver Registration" %}
            <form action="{{ url_for('driver.register_driver') }}" method="POST">
            {% else %}
            <form action="{{ url_for('driver.update_profile') }}" method="POST">
            {% endif %}
                <div class="form-row">
                    <div class="col form-group">
                        <label>License Number: </label>
                        {% if title in "Driver Registration" %}
                            <input name="license-number" id="license-number" type="text" class="form-control" required>
                        {% else %}
                            <input name="license-number" id="license-number" type="text" class="form-control" value="{{ driver.license_number }}"readonly>
                        {% endif %}
                    </div> <!-- form-group end.// -->
                </div> <!-- form-row end.// -->
                <div class="form-group">
                        <label>License Plate: </label>
                        {% if title in "Driver Registration" %}
                        <input name="license-plate" id="license-plate" type="text" class="form-control" placeholder="SXX1234A" required>
                        {% else %}
                        <input name="license-plate" id="license-plate" type="text" class="form-control" placeholder="SXX1234A" value="{{ car.license_plate }}" readonly>
                        {% endif %}
                </div> <!-- form-group end.// -->
                <div class="form-row">
                    <div class="form-group col-md-6">
                          <label>Brand: </label>
                          {% if title in "Driver Registration" %}
                                <input name="brand" id="brand" type="text" class="form-control" required>
                          {% else %}
                                <input name="brand" id="brand" type="text" value="{{ car.brand }}" class="form-control" required>
                          {% endif %}

                    </div> <!-- form-group end.// -->
                    <div class="form-group col-md-6">
                          <label>Model: </label>
                          {% if title in "Driver Registration" %}
                                <input name="model" id="model" type="text" class="form-control" required>
                          {% else %}
                                <input name="model" id="model" type="text" value="{{ car.model }}" class="form-control" required>
                          {% endif %}

                    </div> <!-- form-group end.// -->
                </div>
                <div class="form-group">
                    <div class="form-group">
                        <label>(Optional) Bio: </label>
                        {% if title in "Driver Registration" %}
                            <textarea name="optional-bio" id="optional-bio" class="form-control" type="text" rows="3"></textarea>
                        {% else %}
                            <textarea name="optional-bio" id="optional-bio" class="form-control" type="text" rows="3">{% if driver.optional_bio not in "None" %}
                                {{ driver.optional_bio }}
                            {% endif %}</textarea>
                        {% endif %}
                    </div>
                </div>
                <div class="form-group">
                    <button type="submit" class="btn btn-secondary btn-block">
                        {% if title in "Driver Registration" %}
                            Register as Driver
                        {% else %}
                            Save
                        {% endif %}
                    </button>
                </div> <!-- form-group// -->
                </div> <!-- form-row.// -->
            </form>
            </article> <!-- card-body end .// -->
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
