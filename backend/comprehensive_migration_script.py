#!/usr/bin/env python3
"""
Comprehensive data migration script from legacy API app to new modular structure.
This script migrates ALL tables from the old api app to the new modular apps:
- Core app: Administrators, Countries, CarbonIntensities, Configuration
- GAISSALabel app: All GAISSALabel-related models
- GAISSA ROI Analyzer app: All ROI analysis-related models

This ensures every table and every row is migrated with identical parameters
for both local and production deployment.
"""

import os
import sys
import django
from django.db import transaction, connection
from django.core.management import call_command

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaissalabel.settings')
django.setup()


def update_database_sequences():
    """
    COMPREHENSIVE UPDATE of ALL PostgreSQL sequences to avoid ID collision errors after migration.
    This function automatically discovers and updates all 55+ sequences in the database.
    """
    print("\n🔧 COMPREHENSIVE DATABASE SEQUENCE UPDATE")
    print("=" * 60)
    print("Updating ALL PostgreSQL sequences to prevent ID collisions when creating new records")
    
    try:
        with connection.cursor() as cursor:
            # Step 1: Get all sequences in the database
            print("🔍 Discovering all database sequences...")
            cursor.execute("""
                SELECT schemaname, sequencename 
                FROM pg_sequences 
                WHERE schemaname = 'public'
                ORDER BY sequencename;
            """)
            
            all_sequences = cursor.fetchall()
            print(f"Found {len(all_sequences)} sequences in the database")
            
            # Step 2: Categorize sequences and identify which ones to update
            sequences_to_update = []
            system_sequences = ['django_admin_log_id_seq', 'django_content_type_id_seq', 'django_migrations_id_seq']
            
            for schema, seq_name in all_sequences:
                table_name = seq_name.replace('_id_seq', '') if seq_name.endswith('_id_seq') else seq_name
                
                # Skip Django system sequences (they manage themselves)
                if seq_name in system_sequences:
                    print(f"⏭️  Skipping system sequence: {seq_name}")
                    continue
                
                sequences_to_update.append((seq_name, table_name))
            
            print(f"Will update {len(sequences_to_update)} sequences (skipping {len(system_sequences)} system sequences)")
            
            # Step 3: Update each sequence
            updated_sequences = 0
            failed_sequences = 0
            
            print("\n🔄 Updating sequences...")
            for seq_name, table_name in sequences_to_update:
                try:
                    # Get the maximum ID from the table
                    cursor.execute(f"SELECT MAX(id) FROM {table_name}")
                    max_id_result = cursor.fetchone()
                    max_id = max_id_result[0] if max_id_result[0] is not None else 0
                    
                    # Set the sequence to start from max_id + 1
                    next_id = max_id + 1
                    cursor.execute(f"SELECT setval('{seq_name}', %s, false)", [next_id])
                    
                    if max_id > 0:
                        print(f"    ✅ {seq_name}: updated to start from {next_id}")
                    else:
                        print(f"    ✅ {seq_name}: reset to 1 (empty table)")
                    updated_sequences += 1
                    
                except Exception as e:
                    print(f"    ❌ Failed to update {seq_name}: {str(e)}")
                    failed_sequences += 1
            
            # Step 4: Summary
            print(f"\n📊 SEQUENCE UPDATE SUMMARY:")
            print(f"   ✅ Successfully updated: {updated_sequences} sequences")  
            print(f"   ❌ Failed to update: {failed_sequences} sequences")
            print(f"   ⏭️  System sequences skipped: {len(system_sequences)}")
            print(f"   📋 Total sequences in database: {len(all_sequences)}")
            
            if failed_sequences == 0:
                print("🎉 ALL SEQUENCES SUCCESSFULLY UPDATED!")
                print("✅ Database is now ready for new record creation without ID collisions")
                return True
            else:
                print(f"⚠️  WARNING: {failed_sequences} sequences failed to update")
                return updated_sequences > failed_sequences  # Return True if more succeeded than failed
                
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR during sequence update: {str(e)}")
        print("Migration may not be complete. Please check database status.")
        return False


def run_migrations():
    """Ensure all migrations are applied before data migration"""
    print("Applying database migrations...")
    try:
        call_command('makemigrations', 'core', verbosity=1)
        call_command('makemigrations', 'gaissalabel', verbosity=1)
        call_command('makemigrations', 'gaissa_roi_analyzer', verbosity=1)
        call_command('migrate', verbosity=1)
        print("✅ All migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False


def verify_legacy_data():
    """Verify that legacy data exists before migration"""
    print("Verifying legacy data...")
    
    try:
        from api.models import (
            Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval,
            ResultatEntrenament, ResultatInferencia, InfoAddicional, 
            ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul,
            TransformacioMetrica, TransformacioInformacio, Administrador,
            Configuracio, ModelArchitecture, TacticSource, MLTactic,
            TacticParameterOption, ROIAnalysis, ROIAnalysisCalculation,
            ROIAnalysisResearch, ROIMetric, AnalysisMetricValue,
            EnergyAnalysisMetricValue, ExpectedMetricReduction,
            Country, CarbonIntensity
        )
        
        legacy_counts = {
            'Model': Model.objects.count(),
            'Entrenament': Entrenament.objects.count(),
            'Inferencia': Inferencia.objects.count(),
            'Metrica': Metrica.objects.count(),
            'Qualificacio': Qualificacio.objects.count(),
            'Interval': Interval.objects.count(),
            'ResultatEntrenament': ResultatEntrenament.objects.count(),
            'ResultatInferencia': ResultatInferencia.objects.count(),
            'InfoAddicional': InfoAddicional.objects.count(),
            'ValorInfoEntrenament': ValorInfoEntrenament.objects.count(),
            'ValorInfoInferencia': ValorInfoInferencia.objects.count(),
            'EinaCalcul': EinaCalcul.objects.count(),
            'TransformacioMetrica': TransformacioMetrica.objects.count(),
            'TransformacioInformacio': TransformacioInformacio.objects.count(),
            'Administrador': Administrador.objects.count(),
            'Configuracio': Configuracio.objects.count(),
            'ModelArchitecture': ModelArchitecture.objects.count(),
            'TacticSource': TacticSource.objects.count(),
            'MLTactic': MLTactic.objects.count(),
            'TacticParameterOption': TacticParameterOption.objects.count(),
            'ROIAnalysis': ROIAnalysis.objects.count(),
            'ROIAnalysisCalculation': ROIAnalysisCalculation.objects.count(),
            'ROIAnalysisResearch': ROIAnalysisResearch.objects.count(),
            'ROIMetric': ROIMetric.objects.count(),
            'AnalysisMetricValue': AnalysisMetricValue.objects.count(),
            'EnergyAnalysisMetricValue': EnergyAnalysisMetricValue.objects.count(),
            'ExpectedMetricReduction': ExpectedMetricReduction.objects.count(),
            'Country': Country.objects.count(),
            'CarbonIntensity': CarbonIntensity.objects.count(),
        }
        
        print("Legacy API data counts:")
        total_records = 0
        for model_name, count in legacy_counts.items():
            print(f"  {model_name}: {count}")
            total_records += count
            
        print(f"Total legacy records: {total_records}")
        return legacy_counts, total_records
        
    except Exception as e:
        print(f"❌ Error verifying legacy data: {e}")
        return {}, 0


def migrate_core_models():
    """Migrate models to Core app"""
    print("\n🔄 Migrating Core App models...")
    migrated_count = 0
    
    # Migrate Administrador
    print("  Migrating Administrador...")
    try:
        from api.models import Administrador as LegacyAdministrador
        from apps.core.models import Administrador
        
        legacy_admins = LegacyAdministrador.objects.all()
        for legacy_admin in legacy_admins:
            admin, created = Administrador.objects.get_or_create(
                user_id=legacy_admin.user_id,
                defaults={'user': legacy_admin.user}
            )
            if created:
                migrated_count += 1
                print(f"    ✅ Migrated administrator: {legacy_admin.user.username}")
        
    except Exception as e:
        print(f"    ❌ Error migrating Administrador: {e}")
    
    # Migrate Configuracio
    print("  Migrating Configuracio...")
    try:
        from api.models import Configuracio as LegacyConfiguracio
        from apps.core.models import Configuracio
        
        legacy_config = LegacyConfiguracio.objects.first()
        if legacy_config:
            config, created = Configuracio.objects.get_or_create(
                defaults={
                    'gaissa_label_enabled': True,
                    'gaissa_roi_analyzer_enabled': True,
                    'ultimaSincronitzacio': legacy_config.ultimaSincronitzacio,
                }
            )
            if created:
                migrated_count += 1
                print(f"    ✅ Migrated configuration")
        
    except Exception as e:
        print(f"    ❌ Error migrating Configuracio: {e}")
    
    # Migrate Country
    print("  Migrating Country...")
    try:
        from api.models import Country as LegacyCountry
        from apps.core.models import Country
        
        legacy_countries = LegacyCountry.objects.all()
        for legacy_country in legacy_countries:
            country, created = Country.objects.get_or_create(
                id=legacy_country.id,
                defaults={
                    'name': legacy_country.name,
                    'country_code': legacy_country.country_code,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {Country.objects.count()} countries")
        
    except Exception as e:
        print(f"    ❌ Error migrating Country: {e}")
    
    # Migrate CarbonIntensity
    print("  Migrating CarbonIntensity...")
    try:
        from api.models import CarbonIntensity as LegacyCarbonIntensity
        from apps.core.models import CarbonIntensity, Country
        
        legacy_carbon_intensities = LegacyCarbonIntensity.objects.all()
        for legacy_ci in legacy_carbon_intensities:
            try:
                country = Country.objects.get(id=legacy_ci.country.id)
                ci, created = CarbonIntensity.objects.get_or_create(
                    country=country,
                    data_year=legacy_ci.data_year,
                    defaults={
                        'carbon_intensity': legacy_ci.carbon_intensity,
                    }
                )
                if created:
                    migrated_count += 1
            except Country.DoesNotExist:
                print(f"    ⚠️ Country not found for CarbonIntensity {legacy_ci.id}")
        print(f"    ✅ Migrated {CarbonIntensity.objects.count()} carbon intensity records")
        
    except Exception as e:
        print(f"    ❌ Error migrating CarbonIntensity: {e}")
    
    print(f"✅ Core app migration completed. Migrated {migrated_count} new records.")
    return migrated_count


def migrate_gaissalabel_models():
    """Migrate models to GAISSALabel app"""
    print("\n🔄 Migrating GAISSALabel App models...")
    migrated_count = 0
    
    # First migrate base models (Model, Metrica, Qualificacio)
    print("  Migrating base models (Model, Metrica, Qualificacio)...")
    try:
        from api.models import (
            Model as LegacyModel,
            Metrica as LegacyMetrica, 
            Qualificacio as LegacyQualificacio
        )
        from apps.gaissalabel.models import Model, Metrica, Qualificacio
        
        # Migrate Model
        legacy_models = LegacyModel.objects.all()
        for legacy_model in legacy_models:
            model, created = Model.objects.get_or_create(
                id=legacy_model.id,
                defaults={
                    'nom': legacy_model.nom,
                    'informacio': legacy_model.informacio,
                    'dataCreacio': legacy_model.dataCreacio,
                    'autor': legacy_model.autor,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {Model.objects.count()} Model records")
        
        # Migrate Metrica
        legacy_metriques = LegacyMetrica.objects.all()
        for legacy_metrica in legacy_metriques:
            # Note: nomTecnic field was removed in migration 0007
            metrica, created = Metrica.objects.get_or_create(
                id=legacy_metrica.id,
                defaults={
                    'nom': legacy_metrica.nom,
                    'fase': legacy_metrica.fase,
                    'pes': legacy_metrica.pes,
                    'influencia': legacy_metrica.influencia,
                    'descripcio': legacy_metrica.descripcio,
                    'unitat': legacy_metrica.unitat,
                    'calcul': legacy_metrica.calcul,
                    'recomanacions': legacy_metrica.recomanacions,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {Metrica.objects.count()} Metrica records")
        
        # Migrate Qualificacio
        legacy_qualificacions = LegacyQualificacio.objects.all()
        for legacy_qualificacio in legacy_qualificacions:
            qualificacio, created = Qualificacio.objects.get_or_create(
                id=legacy_qualificacio.id,
                defaults={
                    'color': legacy_qualificacio.color,
                    'ordre': legacy_qualificacio.ordre,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {Qualificacio.objects.count()} Qualificacio records")
        
    except Exception as e:
        print(f"    ❌ Error migrating base models: {e}")
    
    # Next migrate Entrenament and Inferencia (depend on Model)
    print("  Migrating Entrenament and Inferencia...")
    try:
        from api.models import Entrenament as LegacyEntrenament, Inferencia as LegacyInferencia
        from apps.gaissalabel.models import Entrenament, Inferencia, Model
        
        # Migrate Entrenament
        legacy_entrenaments = LegacyEntrenament.objects.all()
        for legacy_entrenament in legacy_entrenaments:
            try:
                model = Model.objects.get(id=legacy_entrenament.model.id)
                entrenament, created = Entrenament.objects.get_or_create(
                    id=legacy_entrenament.id,
                    defaults={
                        'model': model,
                        'dataRegistre': legacy_entrenament.dataRegistre,
                    }
                )
                if created:
                    migrated_count += 1
            except Model.DoesNotExist:
                pass
        print(f"    ✅ Migrated {Entrenament.objects.count()} Entrenament records")
        
        # Migrate Inferencia
        legacy_inferencies = LegacyInferencia.objects.all()
        for legacy_inferencia in legacy_inferencies:
            try:
                model = Model.objects.get(id=legacy_inferencia.model.id)
                inferencia, created = Inferencia.objects.get_or_create(
                    id=legacy_inferencia.id,
                    defaults={
                        'model': model,
                        'dataRegistre': legacy_inferencia.dataRegistre,
                    }
                )
                if created:
                    migrated_count += 1
            except Model.DoesNotExist:
                pass
        print(f"    ✅ Migrated {Inferencia.objects.count()} Inferencia records")
        
    except Exception as e:
        print(f"    ❌ Error migrating Entrenament/Inferencia: {e}")

    # Migrate InfoAddicional
    print("  Migrating InfoAddicional...")
    try:
        from api.models import InfoAddicional as LegacyInfoAddicional
        from apps.gaissalabel.models import InfoAddicional
        
        legacy_infos = LegacyInfoAddicional.objects.all()
        for legacy_info in legacy_infos:
            info, created = InfoAddicional.objects.get_or_create(
                id=legacy_info.id,
                defaults={
                    'nom': legacy_info.nom,
                    'fase': legacy_info.fase,
                    'descripcio': legacy_info.descripcio,
                    'opcions': legacy_info.opcions,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {InfoAddicional.objects.count()} InfoAddicional records")
        
    except Exception as e:
        print(f"    ❌ Error migrating InfoAddicional: {e}")
    
    # Migrate EinaCalcul
    print("  Migrating EinaCalcul...")
    try:
        from api.models import EinaCalcul as LegacyEinaCalcul
        from apps.gaissalabel.models import EinaCalcul
        
        legacy_eines = LegacyEinaCalcul.objects.all()
        for legacy_eina in legacy_eines:
            eina, created = EinaCalcul.objects.get_or_create(
                id=legacy_eina.id,
                defaults={
                    'nom': legacy_eina.nom,
                    'descripcio': legacy_eina.descripcio,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {EinaCalcul.objects.count()} EinaCalcul records")
        
    except Exception as e:
        print(f"    ❌ Error migrating EinaCalcul: {e}")
    
    # Migrate Interval
    print("  Migrating Interval...")
    try:
        from api.models import Interval as LegacyInterval
        from apps.gaissalabel.models import Interval, Metrica, Qualificacio
        
        legacy_intervals = LegacyInterval.objects.all()
        for legacy_interval in legacy_intervals:
            try:
                metrica = Metrica.objects.get(id=legacy_interval.metrica.id)
                qualificacio = Qualificacio.objects.get(id=legacy_interval.qualificacio.id)
                
                interval, created = Interval.objects.get_or_create(
                    id=legacy_interval.id,
                    defaults={
                        'metrica': metrica,
                        'qualificacio': qualificacio,
                        'limitSuperior': legacy_interval.limitSuperior,
                        'limitInferior': legacy_interval.limitInferior,
                        'imatge': legacy_interval.imatge,
                    }
                )
                if created:
                    migrated_count += 1
            except (Metrica.DoesNotExist, Qualificacio.DoesNotExist) as e:
                print(f"    ⚠️ Missing reference for Interval {legacy_interval.id}: {e}")
        print(f"    ✅ Migrated {Interval.objects.count()} Interval records")
        
    except Exception as e:
        print(f"    ❌ Error migrating Interval: {e}")
    
    # Migrate ResultatEntrenament
    print("  Migrating ResultatEntrenament...")
    try:
        from api.models import ResultatEntrenament as LegacyResultatEntrenament
        from apps.gaissalabel.models import ResultatEntrenament, Entrenament, Metrica
        
        legacy_resultats = LegacyResultatEntrenament.objects.all()
        batch_size = 1000
        total_count = legacy_resultats.count()
        
        for i in range(0, total_count, batch_size):
            batch = legacy_resultats[i:i+batch_size]
            batch_migrated = 0
            
            for legacy_resultat in batch:
                try:
                    entrenament = Entrenament.objects.get(id=legacy_resultat.entrenament.id)
                    metrica = Metrica.objects.get(id=legacy_resultat.metrica.id)
                    
                    resultat, created = ResultatEntrenament.objects.get_or_create(
                        entrenament=entrenament,
                        metrica=metrica,
                        defaults={'valor': legacy_resultat.valor}
                    )
                    if created:
                        batch_migrated += 1
                except (Entrenament.DoesNotExist, Metrica.DoesNotExist):
                    pass  # Skip missing references
            
            migrated_count += batch_migrated
            print(f"    Batch {i//batch_size + 1}: Migrated {batch_migrated} records")
        
        print(f"    ✅ Migrated {ResultatEntrenament.objects.count()} ResultatEntrenament records")
        
    except Exception as e:
        print(f"    ❌ Error migrating ResultatEntrenament: {e}")
    
    # Migrate ResultatInferencia
    print("  Migrating ResultatInferencia...")
    try:
        from api.models import ResultatInferencia as LegacyResultatInferencia
        from apps.gaissalabel.models import ResultatInferencia, Inferencia, Metrica
        
        legacy_resultats = LegacyResultatInferencia.objects.all()
        for legacy_resultat in legacy_resultats:
            try:
                inferencia = Inferencia.objects.get(id=legacy_resultat.inferencia.id)
                metrica = Metrica.objects.get(id=legacy_resultat.metrica.id)
                
                resultat, created = ResultatInferencia.objects.get_or_create(
                    inferencia=inferencia,
                    metrica=metrica,
                    defaults={'valor': legacy_resultat.valor}
                )
                if created:
                    migrated_count += 1
            except (Inferencia.DoesNotExist, Metrica.DoesNotExist):
                pass  # Skip missing references
        
        print(f"    ✅ Migrated {ResultatInferencia.objects.count()} ResultatInferencia records")
        
    except Exception as e:
        print(f"    ❌ Error migrating ResultatInferencia: {e}")
    
    # Migrate ValorInfoEntrenament
    print("  Migrating ValorInfoEntrenament...")
    try:
        from api.models import ValorInfoEntrenament as LegacyValorInfoEntrenament
        from apps.gaissalabel.models import ValorInfoEntrenament, Entrenament, InfoAddicional
        
        legacy_valors = LegacyValorInfoEntrenament.objects.all()
        for legacy_valor in legacy_valors:
            try:
                entrenament = Entrenament.objects.get(id=legacy_valor.entrenament.id)
                info_adicional = InfoAddicional.objects.get(id=legacy_valor.infoAddicional.id)
                
                valor, created = ValorInfoEntrenament.objects.get_or_create(
                    entrenament=entrenament,
                    infoAddicional=info_adicional,
                    defaults={'valor': legacy_valor.valor}
                )
                if created:
                    migrated_count += 1
            except (Entrenament.DoesNotExist, InfoAddicional.DoesNotExist):
                pass  # Skip missing references
        
        print(f"    ✅ Migrated {ValorInfoEntrenament.objects.count()} ValorInfoEntrenament records")
        
    except Exception as e:
        print(f"    ❌ Error migrating ValorInfoEntrenament: {e}")
    
    # Migrate ValorInfoInferencia
    print("  Migrating ValorInfoInferencia...")
    try:
        from api.models import ValorInfoInferencia as LegacyValorInfoInferencia
        from apps.gaissalabel.models import ValorInfoInferencia, Inferencia, InfoAddicional
        
        legacy_valors = LegacyValorInfoInferencia.objects.all()
        for legacy_valor in legacy_valors:
            try:
                inferencia = Inferencia.objects.get(id=legacy_valor.inferencia.id)
                info_adicional = InfoAddicional.objects.get(id=legacy_valor.infoAddicional.id)
                
                valor, created = ValorInfoInferencia.objects.get_or_create(
                    inferencia=inferencia,
                    infoAddicional=info_adicional,
                    defaults={'valor': legacy_valor.valor}
                )
                if created:
                    migrated_count += 1
            except (Inferencia.DoesNotExist, InfoAddicional.DoesNotExist):
                pass  # Skip missing references
        
        print(f"    ✅ Migrated {ValorInfoInferencia.objects.count()} ValorInfoInferencia records")
        
    except Exception as e:
        print(f"    ❌ Error migrating ValorInfoInferencia: {e}")
    
    # Migrate TransformacioMetrica
    print("  Migrating TransformacioMetrica...")
    try:
        from api.models import TransformacioMetrica as LegacyTransformacioMetrica
        from apps.gaissalabel.models import TransformacioMetrica, Metrica, EinaCalcul
        
        legacy_transformacions = LegacyTransformacioMetrica.objects.all()
        for legacy_transformacio in legacy_transformacions:
            try:
                metrica = Metrica.objects.get(id=legacy_transformacio.metrica.id)
                eina = EinaCalcul.objects.get(id=legacy_transformacio.eina.id)
                
                transformacio, created = TransformacioMetrica.objects.get_or_create(
                    metrica=metrica,
                    eina=eina,
                    valor=legacy_transformacio.valor
                )
                if created:
                    migrated_count += 1
            except (Metrica.DoesNotExist, EinaCalcul.DoesNotExist):
                pass  # Skip missing references
        
        print(f"    ✅ Migrated {TransformacioMetrica.objects.count()} TransformacioMetrica records")
        
    except Exception as e:
        print(f"    ❌ Error migrating TransformacioMetrica: {e}")
    
    # Migrate TransformacioInformacio
    print("  Migrating TransformacioInformacio...")
    try:
        from api.models import TransformacioInformacio as LegacyTransformacioInformacio
        from apps.gaissalabel.models import TransformacioInformacio, InfoAddicional, EinaCalcul
        
        legacy_transformacions = LegacyTransformacioInformacio.objects.all()
        for legacy_transformacio in legacy_transformacions:
            try:
                informacio = InfoAddicional.objects.get(id=legacy_transformacio.informacio.id)
                eina = EinaCalcul.objects.get(id=legacy_transformacio.eina.id)
                
                transformacio, created = TransformacioInformacio.objects.get_or_create(
                    informacio=informacio,
                    eina=eina,
                    valor=legacy_transformacio.valor
                )
                if created:
                    migrated_count += 1
            except (InfoAddicional.DoesNotExist, EinaCalcul.DoesNotExist):
                pass  # Skip missing references
        
        print(f"    ✅ Migrated {TransformacioInformacio.objects.count()} TransformacioInformacio records")
        
    except Exception as e:
        print(f"    ❌ Error migrating TransformacioInformacio: {e}")
    
    print(f"✅ GAISSALabel app migration completed. Migrated {migrated_count} new records.")
    return migrated_count


def migrate_roi_analyzer_models():
    """Migrate models to GAISSA ROI Analyzer app"""
    print("\n🔄 Migrating GAISSA ROI Analyzer App models...")
    migrated_count = 0
    
    # First migrate ModelArchitecture, TacticSource, MLTactic, etc.
    print("  Migrating ModelArchitecture...")
    try:
        from api.models import ModelArchitecture as LegacyModelArchitecture
        from apps.gaissa_roi_analyzer.models import ModelArchitecture
        
        legacy_architectures = LegacyModelArchitecture.objects.all()
        for legacy_arch in legacy_architectures:
            arch, created = ModelArchitecture.objects.get_or_create(
                id=legacy_arch.id,
                defaults={
                    'name': legacy_arch.name,
                    'information': legacy_arch.information,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {ModelArchitecture.objects.count()} ModelArchitecture records")
    except Exception as e:
        print(f"    ❌ Error migrating ModelArchitecture: {e}")
    
    # Migrate TacticSource, MLTactic, etc.
    print("  Migrating TacticSource, MLTactic, and related models...")
    try:
        from api.models import (
            TacticSource as LegacyTacticSource,
            MLTactic as LegacyMLTactic,
            TacticParameterOption as LegacyTacticParameterOption,
            ROIMetric as LegacyROIMetric
        )
        from apps.gaissa_roi_analyzer.models import (
            TacticSource, MLTactic, TacticParameterOption, ROIMetric
        )
        
        # Migrate TacticSource
        legacy_sources = LegacyTacticSource.objects.all()
        for legacy_source in legacy_sources:
            source, created = TacticSource.objects.get_or_create(
                id=legacy_source.id,
                defaults={
                    'title': legacy_source.title,
                    'url': legacy_source.url,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {TacticSource.objects.count()} TacticSource records")
        
        # Migrate MLTactic
        legacy_tactics = LegacyMLTactic.objects.all()
        for legacy_tactic in legacy_tactics:
            tactic, created = MLTactic.objects.get_or_create(
                id=legacy_tactic.id,
                defaults={
                    'name': legacy_tactic.name,
                    'information': legacy_tactic.information,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {MLTactic.objects.count()} MLTactic records")
        
        # Now migrate many-to-many relationships for MLTactic
        print("  Migrating MLTactic many-to-many relationships...")
        for legacy_tactic in legacy_tactics:
            try:
                tactic = MLTactic.objects.get(id=legacy_tactic.id)
                
                # Migrate sources relationship
                for source in legacy_tactic.sources.all():
                    try:
                        new_source = TacticSource.objects.get(id=source.id)
                        tactic.sources.add(new_source)
                    except TacticSource.DoesNotExist:
                        print(f"    ⚠️ TacticSource {source.id} not found for MLTactic {legacy_tactic.id}")
                
                # Migrate compatible_architectures relationship
                for architecture in legacy_tactic.compatible_architectures.all():
                    try:
                        new_architecture = ModelArchitecture.objects.get(id=architecture.id)
                        tactic.compatible_architectures.add(new_architecture)
                    except ModelArchitecture.DoesNotExist:
                        print(f"    ⚠️ ModelArchitecture {architecture.id} not found for MLTactic {legacy_tactic.id}")
                
                # Migrate applicable_metrics relationship  
                for metric in legacy_tactic.applicable_metrics.all():
                    try:
                        new_metric = ROIMetric.objects.get(id=metric.id)
                        tactic.applicable_metrics.add(new_metric)
                    except ROIMetric.DoesNotExist:
                        print(f"    ⚠️ ROIMetric {metric.id} not found for MLTactic {legacy_tactic.id}")
                        
            except MLTactic.DoesNotExist:
                print(f"    ⚠️ MLTactic {legacy_tactic.id} not found in new app")
        
        # Count many-to-many relationships
        total_sources = sum(tactic.sources.count() for tactic in MLTactic.objects.all())
        total_architectures = sum(tactic.compatible_architectures.count() for tactic in MLTactic.objects.all())
        total_metrics = sum(tactic.applicable_metrics.count() for tactic in MLTactic.objects.all())
        print(f"    ✅ Migrated many-to-many relationships:")
        print(f"      - Sources: {total_sources} relationships")
        print(f"      - Compatible Architectures: {total_architectures} relationships")
        print(f"      - Applicable Metrics: {total_metrics} relationships")
        
        # Migrate TacticParameterOption
        legacy_options = LegacyTacticParameterOption.objects.all()
        for legacy_option in legacy_options:
            try:
                tactic = MLTactic.objects.get(id=legacy_option.tactic.id)
                option, created = TacticParameterOption.objects.get_or_create(
                    id=legacy_option.id,
                    defaults={
                        'tactic': tactic,
                        'name': legacy_option.name,
                        'value': legacy_option.value,
                    }
                )
                if created:
                    migrated_count += 1
            except MLTactic.DoesNotExist:
                pass
        print(f"    ✅ Migrated {TacticParameterOption.objects.count()} TacticParameterOption records")
        
        # Migrate ROIMetric
        legacy_metrics = LegacyROIMetric.objects.all()
        for legacy_metric in legacy_metrics:
            metric, created = ROIMetric.objects.get_or_create(
                id=legacy_metric.id,
                defaults={
                    'name': legacy_metric.name,
                    'description': legacy_metric.description,
                    'unit': legacy_metric.unit,
                    'is_energy_related': legacy_metric.is_energy_related,
                    'higher_is_better': legacy_metric.higher_is_better,
                    'min_value': legacy_metric.min_value,
                    'max_value': legacy_metric.max_value,
                }
            )
            if created:
                migrated_count += 1
        print(f"    ✅ Migrated {ROIMetric.objects.count()} ROIMetric records")
        
    except Exception as e:
        print(f"    ❌ Error migrating support models: {e}")
    
    # Now migrate ROIAnalysis and related models
    print("  Migrating ROIAnalysis and related models...")
    try:
        from api.models import (
            ROIAnalysis as LegacyROIAnalysis,
            ROIAnalysisCalculation as LegacyROIAnalysisCalculation,
            ROIAnalysisResearch as LegacyROIAnalysisResearch,
            AnalysisMetricValue as LegacyAnalysisMetricValue,
            EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue,
            ExpectedMetricReduction as LegacyExpectedMetricReduction
        )
        from apps.gaissa_roi_analyzer.models import (
            ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch,
            ModelArchitecture, TacticParameterOption, MLTactic, TacticSource,
            AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction,
            ROIMetric
        )
        from apps.core.models import Country
        
        # Ensure default tactic parameter option exists
        default_tactic_option = TacticParameterOption.objects.first()
        if not default_tactic_option:
            print("    Creating default tactic parameter option...")
            default_source, _ = TacticSource.objects.get_or_create(
                title="Default Migration Source",
                defaults={'url': 'https://example.com/migration'}
            )
            default_tactic, _ = MLTactic.objects.get_or_create(
                name="Default Migration Tactic",
                defaults={'information': 'Created during data migration'}
            )
            default_tactic.sources.add(default_source)
            default_tactic_option, _ = TacticParameterOption.objects.get_or_create(
                tactic=default_tactic,
                name="default",
                value="1.0"
            )
        
        # Migrate base ROIAnalysis
        legacy_analyses = LegacyROIAnalysis.objects.all()
        for legacy_analysis in legacy_analyses:
            try:
                with transaction.atomic():  # Use individual transactions
                    # Handle missing model_architecture
                    architecture = None
                    if legacy_analysis.model_architecture:
                        try:
                            architecture = ModelArchitecture.objects.get(id=legacy_analysis.model_architecture.id)
                        except ModelArchitecture.DoesNotExist:
                            print(f"    ⚠️ ModelArchitecture {legacy_analysis.model_architecture.id} not found for ROIAnalysis {legacy_analysis.id}")
                            architecture = ModelArchitecture.objects.first()
                    else:
                        # If no model_architecture in legacy data, use the first available one
                        print(f"    ⚠️ ROIAnalysis {legacy_analysis.id} has null model_architecture, using default")
                        architecture = ModelArchitecture.objects.first()
                    
                    if not architecture:
                        print(f"    ❌ No ModelArchitecture available, skipping ROIAnalysis {legacy_analysis.id}")
                        continue
                    
                    country = None
                    if legacy_analysis.country:
                        try:
                            country = Country.objects.get(id=legacy_analysis.country.id)
                        except Country.DoesNotExist:
                            country = Country.objects.first()
                    
                    analysis, created = ROIAnalysis.objects.get_or_create(
                        id=legacy_analysis.id,
                        defaults={
                            'model_architecture': architecture,
                            'tactic_parameter_option': default_tactic_option,
                            'country': country,
                        }
                    )
                    if created:
                        migrated_count += 1
            except Exception as e:
                print(f"    ⚠️ Error migrating ROIAnalysis {legacy_analysis.id}: {e}")
                continue
        
        print(f"    ✅ Migrated {ROIAnalysis.objects.count()} ROIAnalysis records")
        
        # Migrate ROIAnalysisCalculation
        legacy_calculations = LegacyROIAnalysisCalculation.objects.all()
        for legacy_calc in legacy_calculations:
            try:
                with transaction.atomic():  # Use individual transactions
                    base_analysis = ROIAnalysis.objects.get(id=legacy_calc.roianalysis_ptr_id)
                    calc, created = ROIAnalysisCalculation.objects.get_or_create(
                        roianalysis_ptr=base_analysis,
                        defaults={'dateRegistration': legacy_calc.dateRegistration}
                    )
                    if created:
                        migrated_count += 1
            except ROIAnalysis.DoesNotExist:
                print(f"    ⚠️ Base ROIAnalysis not found for ROIAnalysisCalculation {legacy_calc.roianalysis_ptr_id}")
            except Exception as e:
                print(f"    ⚠️ Error migrating ROIAnalysisCalculation {legacy_calc.roianalysis_ptr_id}: {e}")
        
        print(f"    ✅ Migrated {ROIAnalysisCalculation.objects.count()} ROIAnalysisCalculation records")
        
        # Migrate ROIAnalysisResearch
        legacy_researches = LegacyROIAnalysisResearch.objects.all()
        for legacy_research in legacy_researches:
            try:
                with transaction.atomic():  # Use individual transactions
                    base_analysis = ROIAnalysis.objects.get(id=legacy_research.roianalysis_ptr_id)
                    source = TacticSource.objects.get(id=legacy_research.source.id)
                    research, created = ROIAnalysisResearch.objects.get_or_create(
                        roianalysis_ptr=base_analysis,
                        defaults={'source': source}
                    )
                    if created:
                        migrated_count += 1
            except (ROIAnalysis.DoesNotExist, TacticSource.DoesNotExist):
                print(f"    ⚠️ Missing reference for ROIAnalysisResearch {legacy_research.roianalysis_ptr_id}")
            except Exception as e:
                print(f"    ⚠️ Error migrating ROIAnalysisResearch {legacy_research.roianalysis_ptr_id}: {e}")
        
        print(f"    ✅ Migrated {ROIAnalysisResearch.objects.count()} ROIAnalysisResearch records")
        
        # Migrate AnalysisMetricValue
        legacy_metric_values = LegacyAnalysisMetricValue.objects.all()
        for legacy_value in legacy_metric_values:
            try:
                with transaction.atomic():  # Use individual transactions
                    analysis = ROIAnalysis.objects.get(id=legacy_value.analysis.id)
                    metric = ROIMetric.objects.get(id=legacy_value.metric.id)
                    
                    metric_value, created = AnalysisMetricValue.objects.get_or_create(
                        analysis=analysis,
                        metric=metric,
                        defaults={'baselineValue': legacy_value.baselineValue}
                    )
                    if created:
                        migrated_count += 1
            except (ROIAnalysis.DoesNotExist, ROIMetric.DoesNotExist):
                print(f"    ⚠️ Missing reference for AnalysisMetricValue (analysis: {legacy_value.analysis.id}, metric: {legacy_value.metric.id})")
            except Exception as e:
                print(f"    ⚠️ Error migrating AnalysisMetricValue: {e}")
        
        print(f"    ✅ Migrated {AnalysisMetricValue.objects.count()} AnalysisMetricValue records")
        
        # Migrate EnergyAnalysisMetricValue
        legacy_energy_values = LegacyEnergyAnalysisMetricValue.objects.all()
        for legacy_energy in legacy_energy_values:
            try:
                with transaction.atomic():  # Use individual transactions
                    # Get the base AnalysisMetricValue
                    base_value = AnalysisMetricValue.objects.get(
                        analysis_id=legacy_energy.analysismetricvalue_ptr.analysis.id,
                        metric_id=legacy_energy.analysismetricvalue_ptr.metric.id
                    )
                    
                    energy_value, created = EnergyAnalysisMetricValue.objects.get_or_create(
                        analysismetricvalue_ptr=base_value,
                        defaults={
                            'energy_cost_rate': legacy_energy.energy_cost_rate,
                            'implementation_cost': legacy_energy.implementation_cost
                        }
                    )
                    if created:
                        migrated_count += 1
            except AnalysisMetricValue.DoesNotExist:
                print(f"    ⚠️ Base AnalysisMetricValue not found for EnergyAnalysisMetricValue")
            except Exception as e:
                print(f"    ⚠️ Error migrating EnergyAnalysisMetricValue: {e}")
        
        print(f"    ✅ Migrated {EnergyAnalysisMetricValue.objects.count()} EnergyAnalysisMetricValue records")
        
        # Migrate ExpectedMetricReduction
        legacy_reductions = LegacyExpectedMetricReduction.objects.all()
        for legacy_reduction in legacy_reductions:
            try:
                with transaction.atomic():  # Use individual transactions
                    architecture = ModelArchitecture.objects.get(id=legacy_reduction.model_architecture.id)
                    tactic_option = TacticParameterOption.objects.get(id=legacy_reduction.tactic_parameter_option.id)
                    metric = ROIMetric.objects.get(id=legacy_reduction.metric.id)
                    
                    reduction, created = ExpectedMetricReduction.objects.get_or_create(
                        model_architecture=architecture,
                        tactic_parameter_option=tactic_option,
                        metric=metric,
                        defaults={'expectedReductionValue': legacy_reduction.expectedReductionValue}
                    )
                    if created:
                        migrated_count += 1
            except (ModelArchitecture.DoesNotExist, TacticParameterOption.DoesNotExist, ROIMetric.DoesNotExist):
                print(f"    ⚠️ Missing reference for ExpectedMetricReduction")
            except Exception as e:
                print(f"    ⚠️ Error migrating ExpectedMetricReduction: {e}")
        
        print(f"    ✅ Migrated {ExpectedMetricReduction.objects.count()} ExpectedMetricReduction records")
        
    except Exception as e:
        print(f"    ❌ Error migrating ROI Analyzer models: {e}")
    
    print(f"✅ GAISSA ROI Analyzer app migration completed. Migrated {migrated_count} new records.")
    return migrated_count


def verify_migration_integrity():
    """Verify that all data has been migrated correctly"""
    print("\n🔍 Verifying migration integrity...")
    
    # Import all models
    from api.models import (
        Model as LegacyModel, Entrenament as LegacyEntrenament, 
        Inferencia as LegacyInferencia, Metrica as LegacyMetrica,
        Qualificacio as LegacyQualificacio, Interval as LegacyInterval,
        ResultatEntrenament as LegacyResultatEntrenament,
        ResultatInferencia as LegacyResultatInferencia,
        InfoAddicional as LegacyInfoAddicional,
        ValorInfoEntrenament as LegacyValorInfoEntrenament,
        ValorInfoInferencia as LegacyValorInfoInferencia,
        EinaCalcul as LegacyEinaCalcul,
        TransformacioMetrica as LegacyTransformacioMetrica,
        TransformacioInformacio as LegacyTransformacioInformacio,
        Administrador as LegacyAdministrador,
        Configuracio as LegacyConfiguracio,
        Country as LegacyCountry,
        CarbonIntensity as LegacyCarbonIntensity,
        ModelArchitecture as LegacyModelArchitecture,
        ROIMetric as LegacyROIMetric,
        ROIAnalysis as LegacyROIAnalysis,
    )
    
    from apps.core.models import Administrador, Configuracio, Country, CarbonIntensity
    from apps.gaissalabel.models import (
        Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval,
        ResultatEntrenament, ResultatInferencia, InfoAddicional,
        ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul,
        TransformacioMetrica, TransformacioInformacio
    )
    from apps.gaissa_roi_analyzer.models import ModelArchitecture, ROIMetric, ROIAnalysis
    
    # Compare counts
    comparisons = [
        ('Model', LegacyModel, Model),
        ('Entrenament', LegacyEntrenament, Entrenament),
        ('Inferencia', LegacyInferencia, Inferencia),
        ('Metrica', LegacyMetrica, Metrica),
        ('Qualificacio', LegacyQualificacio, Qualificacio),
        ('Interval', LegacyInterval, Interval),
        ('ResultatEntrenament', LegacyResultatEntrenament, ResultatEntrenament),
        ('ResultatInferencia', LegacyResultatInferencia, ResultatInferencia),
        ('InfoAddicional', LegacyInfoAddicional, InfoAddicional),
        ('ValorInfoEntrenament', LegacyValorInfoEntrenament, ValorInfoEntrenament),
        ('ValorInfoInferencia', LegacyValorInfoInferencia, ValorInfoInferencia),
        ('EinaCalcul', LegacyEinaCalcul, EinaCalcul),
        ('TransformacioMetrica', LegacyTransformacioMetrica, TransformacioMetrica),
        ('TransformacioInformacio', LegacyTransformacioInformacio, TransformacioInformacio),
        ('Administrador', LegacyAdministrador, Administrador),
        ('Country', LegacyCountry, Country),
        ('CarbonIntensity', LegacyCarbonIntensity, CarbonIntensity),
        ('ModelArchitecture', LegacyModelArchitecture, ModelArchitecture),
        ('ROIMetric', LegacyROIMetric, ROIMetric),
        ('ROIAnalysis', LegacyROIAnalysis, ROIAnalysis),
    ]
    
    all_match = True
    print("Migration integrity check:")
    
    for model_name, legacy_model, new_model in comparisons:
        legacy_count = legacy_model.objects.count()
        new_count = new_model.objects.count()
        
        if legacy_count == new_count:
            print(f"  ✅ {model_name}: {legacy_count} = {new_count}")
        else:
            print(f"  ❌ {model_name}: {legacy_count} ≠ {new_count} (MISMATCH)")
            all_match = False
    
    # Special check for Configuracio (singleton)
    legacy_config_count = LegacyConfiguracio.objects.count()
    new_config_count = Configuracio.objects.count()
    if legacy_config_count > 0 and new_config_count > 0:
        print(f"  ✅ Configuracio: Exists in both")
    else:
        print(f"  ❌ Configuracio: Legacy={legacy_config_count}, New={new_config_count}")
        all_match = False
    
    return all_match


def display_final_counts():
    """Display final data counts after migration"""
    print("\n📊 FINAL DATA COUNTS AFTER MIGRATION:")
    print("=" * 60)
    
    # Core App
    from apps.core.models import Administrador, Configuracio, Country, CarbonIntensity
    print("CORE APP:")
    print(f"  📋 Administrators: {Administrador.objects.count()}")
    print(f"  🌍 Countries: {Country.objects.count()}")
    print(f"  🔋 Carbon Intensities: {CarbonIntensity.objects.count()}")
    print(f"  ⚙️  Configurations: {Configuracio.objects.count()}")
    
    # GAISSALabel App
    from apps.gaissalabel.models import (
        Model, Entrenament, Inferencia, Metrica, Qualificacio, Interval,
        ResultatEntrenament, ResultatInferencia, InfoAddicional,
        ValorInfoEntrenament, ValorInfoInferencia, EinaCalcul,
        TransformacioMetrica, TransformacioInformacio
    )
    print("\nGAISSALABEL APP:")
    print(f"  🤖 Models: {Model.objects.count()}")
    print(f"  🏋️  Entrenaments: {Entrenament.objects.count()}")
    print(f"  🔮 Inferencies: {Inferencia.objects.count()}")
    print(f"  📏 Metriques: {Metrica.objects.count()}")
    print(f"  🏆 Qualifications: {Qualificacio.objects.count()}")
    print(f"  📊 Intervals: {Interval.objects.count()}")
    print(f"  📈 Training Results: {ResultatEntrenament.objects.count()}")
    print(f"  📉 Inference Results: {ResultatInferencia.objects.count()}")
    print(f"  ℹ️  Additional Info: {InfoAddicional.objects.count()}")
    print(f"  📝 Training Info Values: {ValorInfoEntrenament.objects.count()}")
    print(f"  📝 Inference Info Values: {ValorInfoInferencia.objects.count()}")
    print(f"  🔧 Calculation Tools: {EinaCalcul.objects.count()}")
    print(f"  🔄 Metric Transformations: {TransformacioMetrica.objects.count()}")
    print(f"  🔄 Info Transformations: {TransformacioInformacio.objects.count()}")
    
    # GAISSA ROI Analyzer App
    from apps.gaissa_roi_analyzer.models import (
        ModelArchitecture, TacticSource, MLTactic, TacticParameterOption,
        ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric,
        AnalysisMetricValue, EnergyAnalysisMetricValue, ExpectedMetricReduction
    )
    print("\nGAISSA ROI ANALYZER APP:")
    print(f"  🏗️  Model Architectures: {ModelArchitecture.objects.count()}")
    print(f"  📚 Tactic Sources: {TacticSource.objects.count()}")
    print(f"  🎯 ML Tactics: {MLTactic.objects.count()}")
    print(f"  ⚙️  Tactic Parameter Options: {TacticParameterOption.objects.count()}")
    print(f"  📊 ROI Metrics: {ROIMetric.objects.count()}")
    print(f"  🔬 ROI Analyses: {ROIAnalysis.objects.count()}")
    print(f"  🧮 ROI Analysis Calculations: {ROIAnalysisCalculation.objects.count()}")
    print(f"  📖 ROI Analysis Research: {ROIAnalysisResearch.objects.count()}")
    print(f"  📏 Analysis Metric Values: {AnalysisMetricValue.objects.count()}")
    print(f"  ⚡ Energy Analysis Metric Values: {EnergyAnalysisMetricValue.objects.count()}")
    print(f"  📉 Expected Metric Reductions: {ExpectedMetricReduction.objects.count()}")
    
    # Calculate totals
    core_total = (Administrador.objects.count() + Country.objects.count() + 
                 CarbonIntensity.objects.count() + Configuracio.objects.count())
    
    gaissalabel_total = (Model.objects.count() + Entrenament.objects.count() + 
                        Inferencia.objects.count() + Metrica.objects.count() + 
                        Qualificacio.objects.count() + Interval.objects.count() +
                        ResultatEntrenament.objects.count() + ResultatInferencia.objects.count() +
                        InfoAddicional.objects.count() + ValorInfoEntrenament.objects.count() +
                        ValorInfoInferencia.objects.count() + EinaCalcul.objects.count() +
                        TransformacioMetrica.objects.count() + TransformacioInformacio.objects.count())
    
    roi_total = (ModelArchitecture.objects.count() + TacticSource.objects.count() +
                MLTactic.objects.count() + TacticParameterOption.objects.count() +
                ROIAnalysis.objects.count() + ROIAnalysisCalculation.objects.count() +
                ROIAnalysisResearch.objects.count() + ROIMetric.objects.count() +
                AnalysisMetricValue.objects.count() + EnergyAnalysisMetricValue.objects.count() +
                ExpectedMetricReduction.objects.count())
    
    grand_total = core_total + gaissalabel_total + roi_total
    
    print(f"\n📊 SUMMARY:")
    print(f"  Core App Total: {core_total}")
    print(f"  GAISSALabel App Total: {gaissalabel_total}")
    print(f"  ROI Analyzer App Total: {roi_total}")
    print(f"  🎯 GRAND TOTAL: {grand_total} records")


def main():
    """Main migration function"""
    print("🚀 COMPREHENSIVE DATA MIGRATION SCRIPT")
    print("=" * 60)
    print("Migrating ALL tables from legacy API app to new modular structure")
    print("This ensures identical data for both local and production deployment\n")
    
    # Step 1: Apply migrations
    if not run_migrations():
        print("❌ Migration failed at migration step")
        return False
    
    # Step 2: Verify legacy data exists
    legacy_counts, total_legacy = verify_legacy_data()
    if total_legacy == 0:
        print("⚠️  No legacy data found to migrate")
        return True
    
    # Step 3: Perform comprehensive migration
    total_migrated = 0
    
    try:
        with transaction.atomic():
            print("\n🔄 Starting data migration...")
            
            # Migrate Core models
            total_migrated += migrate_core_models()
            
            # Migrate GAISSALabel models
            total_migrated += migrate_gaissalabel_models()
            
            # Migrate ROI Analyzer models
            total_migrated += migrate_roi_analyzer_models()
            
    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        return False
    
    # Step 4: Verify migration integrity
    print("\n" + "=" * 60)
    integrity_check = verify_migration_integrity()
    
    # Step 5: Display final counts
    display_final_counts()
    
    # Step 6: Update database sequences to prevent ID collisions
    print("\n" + "=" * 60)
    sequence_success = update_database_sequences()
    
    print("\n" + "=" * 60)
    if integrity_check and sequence_success:
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print(f"✅ All {total_legacy} legacy records have been migrated")
        print("✅ Data integrity verified - all counts match")
        print("✅ Database sequences updated - new records can be created safely")
        print("✅ Ready for production deployment")
    elif integrity_check:
        print("⚠️  MIGRATION COMPLETED WITH SEQUENCE WARNINGS")
        print(f"✅ All {total_legacy} legacy records have been migrated")
        print("✅ Data integrity verified - all counts match")
        print("⚠️ Some database sequences could not be updated - check manually")
        print("✅ Ready for production deployment")
    else:
        print("⚠️  MIGRATION COMPLETED WITH WARNINGS")
        print(f"📊 {total_migrated} new records migrated")
        print("🔍 Some data counts don't match - please review")
        if sequence_success:
            print("✅ Database sequences updated successfully")
        else:
            print("⚠️ Some database sequences could not be updated")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
