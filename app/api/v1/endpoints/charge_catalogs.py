from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import charge_catalog_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.charge_catalog import ChargeCatalogCreate, ChargeCatalogRead, ChargeCatalogUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{charge_catalog_id}", response_model=ChargeCatalogRead, description="Get a charge_catalog by ID")
def get_charge_catalog(
    charge_catalog_id: int, db: Session = Depends(get_db)
) -> ChargeCatalogRead:
    charge_catalog = charge_catalog_service.get_charge_catalog(db, charge_catalog_id)
    if charge_catalog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalog not found")
    return charge_catalog


@router.get("", response_model=list[ChargeCatalogRead], description="List all charge_catalogs")
def get_charge_catalogs(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ChargeCatalogRead]:
    charge_catalogs = charge_catalog_service.get_charge_catalogs(db, skip=skip, limit=limit)
    return list(charge_catalogs)


@router.post(
    "", response_model=ChargeCatalogRead, status_code=status.HTTP_201_CREATED,
    description="Create a new charge_catalog"
)
def create_charge_catalog(
    charge_catalog_in: ChargeCatalogCreate, db: Session = Depends(get_db)
) -> ChargeCatalogRead:
    charge_catalog = charge_catalog_service.create_charge_catalog(db, charge_catalog_in)
    return charge_catalog


@router.put(
    "/{charge_catalog_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a charge_catalog by ID"
)
def update_charge_catalog(
    charge_catalog_id: int, charge_catalog_in: ChargeCatalogUpdate, db: Session = Depends(get_db)
) -> Response:
    charge_catalog = charge_catalog_service.get_charge_catalog(db, charge_catalog_id)
    if charge_catalog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalog not found")
    charge_catalog_service.update_charge_catalog(db, charge_catalog, charge_catalog_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{charge_catalog_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a charge_catalog by ID")
def delete_charge_catalog(
    charge_catalog_id: int, db: Session = Depends(get_db)
) -> Response:
    charge_catalog = charge_catalog_service.get_charge_catalog(db, charge_catalog_id)
    if charge_catalog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalog not found")

    try:
        charge_catalog_service.delete_charge_catalog(db, charge_catalog)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
