from flask_restful import Resource
from flask import request, current_app
from main.mail.functions import sendMail


class Contacto(Resource):
    def post(self):
        data = request.get_json()
        nombre = (data.get("nombre") or "").strip()
        email = (data.get("email") or "").strip()
        mensaje = (data.get("mensaje") or "").strip()

        if not nombre or not email or not mensaje:
            return {"error": "nombre, email y mensaje son requeridos"}, 400

        gym_email = current_app.config.get("MAIL_USERNAME")

        sent = sendMail(
            [gym_email],
            f"📬 Consulta desde GOL GYM — {nombre}",
            "contacto",
            nombre=nombre,
            email=email,
            mensaje=mensaje,
        )

        if sent:
            return {"message": "Mensaje enviado correctamente. Te responderemos a la brevedad."}, 200
        return {"error": "No se pudo enviar el mensaje. Intenta más tarde."}, 500
