import smtplib as s
ob = s.SMTP("smtp.gmail.com", 587)
ob.starttls()
ob.login("aspire.doctor.appointment@gmail.com", "healthcareusingrasa0782#")


def email(name, number, email_id, age, gender, reason, time):
    Name = name
    Email = email_id
    Mb_num = number
    Age = age
    Gender = gender
    Reason = reason
    Time = time

    subject = "Appointment Confirmation Details"
    body = "Name: {}\nNumber: {}\nAge: {}\nGender: {}\nReason: {}\nTime: {}\nYour appointment for tomorrow is confirmed".format(Name, Mb_num, Age, Gender, Reason, Time)

    message = "Subject:{}\n\n{}".format(subject, body)

    ob.sendmail("aspire.doctor.appointment@gmail.com", Email, message)
    print("Sent successfully")
    ob.quit()
    return "success"

# Name = "Karan"
# Mb_num = 123
#
#
# subject = "Something"
# body = "Name: {}\nNumber: {}\nyour appointment is confirmed for so an so time".format(Name, Mb_num)
# message = "Subject:{}\n\n{}".format(subject, body)
# print(message)