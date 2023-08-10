# Diccionario de Datos

 
* Business_Google_Yelp
  
ID_Business : ID_Business : String, id del local.

Name : String, nombre del local.

Address : String, dirección del local.

City: String, ciudad donde se encuentra el local.

State : String, estado donde se encuentra el local.

Postal_code : INT, codigo postal del local.

Category : String, categoria del local.

Stars : Float, promedio de calificaciones al local.

Review_count : INT, total de reviews al local.

Delivery : INT, servicio de delivery disponible o no.

APP : Aplicación donde se encuentra al local.

 

* Review_Google_Yelp
  
ID_Business : String, id del local.

State : String, estado donde se encuentra el local.

User_ID : Float, id del usuario.

Stars : Int, calificación otorgada por el usuario de 1 a 5.

Text: Reseña otrogada por el usuario.

Date: Fecha de la review del usuario.

APP: Aplicación usada para dar la review.



* Turismo

State: String, estado en donde se generaron los gastos en turismo

USDBil: INT, monto en billones de dolares

Year: INT, año de gastos en turismo



* Emisiones

State: String, estado en donde se generaron las emisiones

CO2 Emissions: float, emisiones de carbono generadas



* Food_waste

State: String, estado en donde se generaron los desperdicios de alimentos

Rank: INT, posición de los estados que más desperdicios de alimentos generan

Tons in M: INT, cantidad de desperdicios generados en millones de toneladas



* State_data

State: String, estados

GDP: INT, producto bruto interno en dólares  para el 2022

Población: INT, población total para el 2022

Personal_Income: INT, ingresos personales en dólares para el 2022 

Min_wage: salario mínimo por hora para el 2022

Average_rent: renta promedio para el 2022

Average_taxes: impuestos promedio para el 2022

Fastfood_percapita: float, fastfood percapita para el 2022



* Menu

State: String, estados

Menu_promedio: float, menu promedio para el 2022
