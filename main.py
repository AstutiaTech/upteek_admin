from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import sys, traceback


from routers.authentication import auth
from routers.user import profile
from routers.misc import geo
from routers.misc import merch
from routers.inventory import category
from routers.user import main as users

#system routes
from routers import seed

# Main app section here
app = FastAPI(title="Upteek Admin")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(geo.router)
app.include_router(merch.router)
app.include_router(category.router)
app.include_router(users.router)

#system routes
app.include_router(seed.router)

#Test routers
# app.include_router(external.router)

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        return response
    except Exception as e:
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        print(err)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder({"detail": str(err)}))


app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World! Upteek Admin"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, "url": request.base_url}),
    )

add_pagination(app)