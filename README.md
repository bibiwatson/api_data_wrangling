
# Proyecto Final del Módulo Kata Data Wrangling

Api que muestra la lista de Expansiones y Cartas del juego de cartas de One Piece

### En Vivo
[https://emmacolorado-katadatawrangling31.glitch.me/](https://emmacolorado-katadatawrangling31.glitch.me/)

# API Endpoints

| HTTP Verbs | Endpoints | Descripción |  
| --- | --- | --- |  
| GET | /sets | Muestra la lista completa de las expansiones existentes |  
| GET | /set/:id_set | Muestra la lista de las cartas que pertenecen a una expansión |
| GET | /cards| Muestra la lista de las cartas encontradas de acuerdo a los filtros utilizados

#### GET /sets
##### Parámetros
No es necesario especificar parámetros

##### Response

```
Status Code 200
{
	success : boolean,
	msg		: string,
	data	: array
}
```

#### GET /set/:id_set
##### Parámetros
| Parámetro | Tipo | Requerido |  
| --- | --- | --- |  
| id_set | int | Obligatorio |  


### Responses
El api devuelve los datos con el siguiente formato
```
{
	success : boolean,
	msg		: string,
	data	: array,
	set_id	: int,
	set_name: string
}
```

#### GET /cards
##### Parámetros
Se utilizan query params y por lo menos un parámetro es requerido

| Parámetro | Tipo | Requerido |  Descripción |
| --- | --- | --- | --- | 
| qstring | String | Opcional |  Texto que se buscará en el nombre, efecto o trigger de las cartas. Se busca que el qstring coincida con una parte del texto solamente |
| rarity | String | Opcional | Rareza de la carta (L,R,C,SR,SEC, SP CARD, UC, P)|
| card_type | String | Opcional | Tipo de Carta (LEADER, CHARACTER, EVENT, STAGE)

```
qstring = nami
rarity = L
card_type = LEADER

SELECT * FROM cards WHERE (name LIKE '%nami%' OR effect like '%nami%' OR trigger LIKE '%nami%') AND rarity = 'L' AND card_type = 'LEADER'
```


### Responses
El api devuelve los datos con el siguiente formato
```
{
	success : boolean,
	msg		: string,
	data	: array
}
```
En dado caso que exista un error solamente se omitirá "data"


### Error Responses
En caso de algún error el api responderá con un código 400 o 500, en ambos casos el formato será el siguiente

```
Status Code 400/500
{
	success	: boolean,
	msg		: string
}
```
