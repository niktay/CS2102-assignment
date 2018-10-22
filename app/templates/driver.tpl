<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../../../favicon.ico">

    <title>CS2102</title>

    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="{{ url_for('static',filename='styles/dashboard.css') }}" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">CS2102</a>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link active" href="#">
                  <span data-feather="users"></span>
                  Accounts <span class="sr-only">(current)</span>
                </a>
              </li>
            </ul>
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
              <span>Saved reports</span>
              <a class="d-flex align-items-center text-muted" href="#">
                <span data-feather="plus-circle"></span>
              </a>
            </h6>
          </div>
        </nav>

        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          </div>
     <div class="row justify-content-center">
            <div class="col-md-6">
            <div class="card">
            <header class="card-header">
                <h4 class="card-title mt-2">{{title}}</h4>
            </header>

            {% if is_view %}
                {% if is_success %}
                <div class="alert alert-success" role="alert">
                    You have successfully registered with us since {{driver[2]}}
                </div>

                {% else %}
                <div class="alert alert-danger" role="alert">
                    An error has occured.
                </div>

                {% endif %}

            {% endif %}

            <article class="card-body">
            {% if title in "Driver Registration" %}
            <form action="{{ url_for('driver.register_driver') }}" method="POST">
            {% else %}
            <form action="{{ url_for('driver.update_profile') }}" method="POST">
            {% endif %}

                <div class="form-row">
                    <div class="col form-group">
                        <label>License Number</label>
                        {% if title in "Driver Registration" %}
                            <input name="license-number" id="license-number" type="text" class="form-control" required>
                        {% else %}
                            <input name="license-number" id="license-number" type="text" value ={{driver[0]}} class="form-control" readonly>
                        {% endif %}
                    </div> <!-- form-group end.// -->
                </div> <!-- form-row end.// -->
                <div class="form-group">
                        <label>License Plate</label>
                        {% if title in "Driver Registration" %}
                        <input name="license-plate" id="license-plate" type="text" class="form-control" placeholder="SXX1234A" required>
                        {% else %}
                        <input name = "license-plate" id="license-plate" type="text" class="form-control" value={{car[0]}} readonly>
                        {% endif %}
                </div> <!-- form-group end.// -->
                <div class="form-row">
                    <div class="form-group col-md-6">
                          <label>Brand of Car</label>
                          {% if title in "Driver Registration" %}
                                <input name="brand" id="brand" type="text" class="form-control" required>
                          {% else %}
                                <input name="brand" id="brand" type="text" value={{car[1]}} class="form-control" required>
                          {% endif %}

                    </div> <!-- form-group end.// -->
                    <div class="form-group col-md-6">
                          <label>Model of Car</label>
                          {% if title in "Driver Registration" %}
                                <input name="model" id="model" type="text" class="form-control" required>
                          {% else %}
                                <input name="model" id="model" type="text" value={{car[2]}} class="form-control" required>
                          {% endif %}

                    </div> <!-- form-group end.// -->
                </div>
                <div class="form-group">
                    <div class="form-group">
                        <label>(Optional) Bio</label>
                        {% if title in "Driver Registration" %}
                            <textarea name="optional-bio" id="optional-bio" class="form-control" type="text" rows="3"></textarea>
                        {% else %}
                            <textarea name="optional-bio" id="optional-bio" class="form-control" type="text" rows="3">{{driver[3]}}</textarea>
                        {% endif %}
                    </div>
                </div>
                <div class="form-group">
                    <button type="submit" class="btn btn-primary btn-block">
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
