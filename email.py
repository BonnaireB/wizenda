# coding: utf8

# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    # email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])

	def __init__(self, email, url):
		self.email = email
		self.url = url

	def send_msg(self, email, url):
		source_address = "benjisosoph@gmail.com"
		destination_address = email
		body = url
		subject = "Reset password"

		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = source_address
		msg['To'] = destination_address

		msg.attach(MIMEText(body, 'plain'))

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(source_address, "labasecesttoi")

		text = msg.as_string()
		server.sendmail(source_address, destination_address, text)
		server.quit()