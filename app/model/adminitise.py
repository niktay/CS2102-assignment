from model.model import Model


class Adminitise(Model):

    def __init__(self, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.new_admin = kwargs.get('new-admin', None)

    def _validate(self):
        return any([
            self.new_admin,
        ])

    def save(self):
        if not self._validate():
            # TODO(Lucy): Throw some error/log
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE account SET is_admin = NOT is_admin WHERE username = "
                f"'{self.new_admin}';",
            )
            self.conn.commit()
            return True
        except Exception as e:
            # TODO(Lucy): Error handling/logging
            print(e)
        return False

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                                Adminitise
--------------------------------------------------------------------------------
new_admin: {self.new_admin}
--------------------------------------------------------------------------------
"""
        return output
