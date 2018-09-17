<!DOCTYPE html>
<html>
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <body>
        <h1>{{table_name}}</h1>
        <table class="table table-bordered">
            <thead>
                <tr>
                    {% for heading in headings %}
                        <th scope="col">{{heading[0]}}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
            {% for result in results %}
                <tr>
                    {% for field in result %}
                        <td>{{field}}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </body>
</html>
