<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-32x32.png') }}" sizes="32x32" />
	<link rel="icon" type="image/png" href="{{ url_for('static', filename='assets/favicon-16x16.png') }}" sizes="16x16" />

    <title>CS2102</title>

    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="{{ url_for('static',filename='styles/dashboard.css') }}" rel="stylesheet">
<link href='https://fonts.googleapis.com/css?family=Nova+Flat' rel='stylesheet' type='text/css'>
  </head>

  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">CS2102</a>
        <form action="/" method="POST" style="width: 100%">
            <input class="form-control form-control-dark w-100" type="text" name="command" placeholder="Command" aria-label="Command">
        </form>
      <ul class="navbar-nav px-3">
        <li class="nav-item text-nowrap">
          <a class="nav-link" href="#">Sign out</a>
        </li>
      </ul>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('admin.view_dashboard') }}">
                  <span data-feather="users"></span>
                  Dashboard <span class="trending-up"></span>
               </a>
              </li>
            </ul>
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link active" href="{{ url_for('adminitise.view_adminitise') }}">
                  <span data-feather="shield"></span>
                  Adminitise <span class="trending-up"></span>
               </a>
              </li>
            </ul>
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
              <span>Table Overview</span>
              <a class="d-flex align-items-center text-muted" href="#">
                <span data-feather="database"></span>
              </a>
            </h6>

            <ul class="nav flex-column mb-2">
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('admin.view_table', table_name='account') }}">
                  <span data-feather="users"></span>
                  Accounts
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('admin.view_table', table_name='advertisement') }}">
                  <span data-feather="tv"></span>
                  Advertisements
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('admin.view_table', table_name='bid') }}">
                  <span data-feather="dollar-sign"></span>
                  Bids
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{ url_for('admin.view_table', table_name='ride') }}">
                  <span data-feather="navigation"></span>
                  Rides
                </a>
              </li>
            </ul>
          </div>
        </nav>

<main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          </div>
    <div class="row justify-content-center">
            <div class="col-md-6">
            <div class="card">
            <header class="card-header">
                <h4 class="card-title mt-2">Adminitise</h4>
            </header>

            {% if is_view %}
                {% if is_success %}
                <div class="alert alert-success" role="alert">
                    Successfully adminitised.
                </div>

                {% else %}
                <div class="alert alert-danger" role="alert">
                    Failed to adminitise.
                </div>

                {% endif %}

            {% endif %}

            <article class="card-body">
            <form action="{{ url_for('adminitise.adminitise_account') }}" method="POST">
                <div class="form-row">
                    <div class="col form-group">
                        <label>Username:</label>
                          <input name="username" id="username" type="text" class="form-control" required>
                    </div> <!-- form-group end.// -->
                </div> <!-- form-row end.// -->
               <div class="form-group">
                    <button type="submit" class="btn btn-primary btn-block">Adminitise</button>
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
