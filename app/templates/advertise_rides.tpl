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
                <a class="nav-link" href="{{ url_for('ride.view_upcoming') }}">
                  <span data-feather="clock"></span>
                  	Scheduled Rides<span class="sr-only"></span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('ride.view_history') }}">
                  <span data-feather="archive"></span>
                  	Ride History<span class="sr-only"></span>
                </a>
              </li>
              {% if driver %}
              <li class="nav-item">
                <a class="nav-link active" href="{{ url_for('advertisement.view_own_advertisements') }}">
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
                  <div class="col-md-10">
                  <div class="card" style="margin-top: 2%">
                    <header class="card-header" style="background: #3b4249; color: white; font-weight: bold;">
                    <h4 class="card-title mt-2">Manage Advertisements</h4>

                </header>
					<article class="card-body">
                     <table class="table table-striped table-sm">
						{% if advertisements %}
                        <thead style="background: #3b4249; color: white; font-weight: bold;">
						  <th scope="col">Date and Time</th>
						  <th scope="col">Origin</th>
						  <th scope="col">Destination</th>
						  <th scope="col">Highest Bid</th>
						  <th scope="col">Status</th>
						  <th scope="col">End Bidding</th>
                        </thead>
                        <tbody>
						   {% for advertisement in advertisements %}
						   <tr>
							  <td>{{ advertisement.start_timestamp }}</td>
							  <td>{{ advertisement.origin }}</td>
							  <td>{{ advertisement.destination }}</td>
							  <td>${{ highest_bid(advertisement).price if highest_bid(advertisement).price else '0' }}.00</td>
							  <td>{% if advertisement.active %}
									<span class="badge badge-success" style="padding: 0.3rem;">Open</span>
								  {% else %}
									<span class="badge badge-danger" style="padding: 0.3rem;">Closed</span>
								  {% endif %}
							  </td>
							  <td>
								<form action="{{ url_for('advertisement.end_bidding') }}" method="POST">
									<input type="hidden" name="start-timestamp" value="{{ advertisement.start_timestamp }}" />
									<input type="hidden" name="license-number" value="{{ advertisement.license_number }}" />
								{% if advertisement.active %}
									<input type="submit" value="End Bidding" class="btn btn-secondary btn-block" style="padding: 2px 6px 2px 6px; font-size: 0.9rem;"/>
								  {% else %}
									<input type="submit" value="End Bidding" class="btn btn-secondary btn-block" style="padding: 2px 6px 2px 6px; font-size: 0.9rem;" disabled/>
								  {% endif %}
								</form>
							</td>
						   </tr>
						   {% endfor %}
					   {% endif %}
                        </tbody>
                     </table>
					</article>
                     <div class="border-top card-body text-center" style="solid #444444!important; font-weight: bold;"><a href="{{ url_for('advertisement.create_advertisement') }}">Create Advertisement</a></div>
                    </div>
                     </div>
                  </div>
               </div>
               <!-- col.//-->
               <!-- row.//-->
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
