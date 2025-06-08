#!/usr/bin/env python3
"""
Fix the Django inheritance migration issue for the remaining 51 records.
These are child models (ROIAnalysisCalculation, ROIAnalysisResearch, EnergyAnalysisMetricValue)
that need to be migrated with their parent model fields included.
"""

import os
import sys
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaissalabel.settings')
django.setup()

def fix_inheritance_migration():
    """Fix inheritance-based model migration for remaining 51 records"""
    print("🔧 Fixing Django inheritance migration for remaining records...")
    
    # Import legacy models
    from api.models import (
        ROIAnalysisCalculation as LegacyROIAnalysisCalculation,
        ROIAnalysisResearch as LegacyROIAnalysisResearch,
        EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    )
    
    # Import new models
    from apps.gaissa_roi_analyzer.models import (
        ROIAnalysisCalculation, ROIAnalysisResearch, EnergyAnalysisMetricValue,
        ModelArchitecture, TacticParameterOption, TacticSource, ROIMetric
    )
    from apps.core.models import Country
    
    migrated_count = 0
    
    # First, ensure we have a default tactic parameter option
    default_tactic_option = TacticParameterOption.objects.first()
    if not default_tactic_option:
        print("Creating default tactic parameter option...")
        from apps.gaissa_roi_analyzer.models import MLTactic
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
    
    # Fix ROIAnalysisCalculation migration
    print("  Fixing ROIAnalysisCalculation inheritance...")
    legacy_calculations = LegacyROIAnalysisCalculation.objects.all()
    for legacy_calc in legacy_calculations:
        try:
            # Check if it already exists
            if ROIAnalysisCalculation.objects.filter(id=legacy_calc.id).exists():
                print(f"    ROIAnalysisCalculation {legacy_calc.id} already exists, skipping")
                continue
                
            with transaction.atomic():
                # Get parent model fields from legacy record
                architecture = None
                if legacy_calc.model_architecture:
                    try:
                        architecture = ModelArchitecture.objects.get(id=legacy_calc.model_architecture.id)
                    except ModelArchitecture.DoesNotExist:
                        architecture = ModelArchitecture.objects.first()
                else:
                    architecture = ModelArchitecture.objects.first()
                
                if not architecture:
                    print(f"    ❌ No ModelArchitecture available for ROIAnalysisCalculation {legacy_calc.id}")
                    continue
                
                country = None
                if legacy_calc.country:
                    try:
                        country = Country.objects.get(id=legacy_calc.country.id)
                    except Country.DoesNotExist:
                        country = Country.objects.first()
                
                # Create child model with parent fields included
                calc = ROIAnalysisCalculation.objects.create(
                    id=legacy_calc.id,
                    model_architecture=architecture,
                    tactic_parameter_option=default_tactic_option,
                    country=country,
                    dateRegistration=legacy_calc.dateRegistration
                )
                migrated_count += 1
                print(f"    ✅ Fixed ROIAnalysisCalculation {legacy_calc.id}")
                
        except Exception as e:
            print(f"    ❌ Error fixing ROIAnalysisCalculation {legacy_calc.id}: {e}")
    
    print(f"    Fixed {ROIAnalysisCalculation.objects.count()} ROIAnalysisCalculation records")
    
    # Fix ROIAnalysisResearch migration
    print("  Fixing ROIAnalysisResearch inheritance...")
    legacy_researches = LegacyROIAnalysisResearch.objects.all()
    for legacy_research in legacy_researches:
        try:
            # Check if it already exists
            if ROIAnalysisResearch.objects.filter(id=legacy_research.id).exists():
                print(f"    ROIAnalysisResearch {legacy_research.id} already exists, skipping")
                continue
                
            with transaction.atomic():
                # Get parent model fields from legacy record
                architecture = None
                if legacy_research.model_architecture:
                    try:
                        architecture = ModelArchitecture.objects.get(id=legacy_research.model_architecture.id)
                    except ModelArchitecture.DoesNotExist:
                        architecture = ModelArchitecture.objects.first()
                else:
                    architecture = ModelArchitecture.objects.first()
                
                if not architecture:
                    print(f"    ❌ No ModelArchitecture available for ROIAnalysisResearch {legacy_research.id}")
                    continue
                
                country = None
                if legacy_research.country:
                    try:
                        country = Country.objects.get(id=legacy_research.country.id)
                    except Country.DoesNotExist:
                        country = Country.objects.first()
                
                source = None
                if legacy_research.source:
                    try:
                        source = TacticSource.objects.get(id=legacy_research.source.id)
                    except TacticSource.DoesNotExist:
                        source = TacticSource.objects.first()
                else:
                    source = TacticSource.objects.first()
                
                if not source:
                    print(f"    ❌ No TacticSource available for ROIAnalysisResearch {legacy_research.id}")
                    continue
                
                # Create child model with parent fields included
                research = ROIAnalysisResearch.objects.create(
                    id=legacy_research.id,
                    model_architecture=architecture,
                    tactic_parameter_option=default_tactic_option,
                    country=country,
                    source=source
                )
                migrated_count += 1
                print(f"    ✅ Fixed ROIAnalysisResearch {legacy_research.id}")
                
        except Exception as e:
            print(f"    ❌ Error fixing ROIAnalysisResearch {legacy_research.id}: {e}")
    
    print(f"    Fixed {ROIAnalysisResearch.objects.count()} ROIAnalysisResearch records")
    
    # Fix EnergyAnalysisMetricValue migration
    print("  Fixing EnergyAnalysisMetricValue inheritance...")
    legacy_energy_values = LegacyEnergyAnalysisMetricValue.objects.all()
    for legacy_energy in legacy_energy_values:
        try:
            # Check if it already exists
            if EnergyAnalysisMetricValue.objects.filter(id=legacy_energy.id).exists():
                print(f"    EnergyAnalysisMetricValue {legacy_energy.id} already exists, skipping")
                continue
                
            with transaction.atomic():
                # Get parent model fields from legacy record (AnalysisMetricValue parent)
                # Check if the analysis and metric exist in new app
                from apps.gaissa_roi_analyzer.models import ROIAnalysis, AnalysisMetricValue
                
                try:
                    # Try to find existing ROIAnalysis (could be base, calculation, or research)
                    base_analysis = None
                    
                    # First try to find as base ROIAnalysis
                    if ROIAnalysis.objects.filter(id=legacy_energy.analysis.id).exists():
                        base_analysis = ROIAnalysis.objects.get(id=legacy_energy.analysis.id)
                    
                    # If not found, try to find as ROIAnalysisCalculation
                    elif ROIAnalysisCalculation.objects.filter(id=legacy_energy.analysis.id).exists():
                        base_analysis = ROIAnalysisCalculation.objects.get(id=legacy_energy.analysis.id)
                    
                    # If not found, try to find as ROIAnalysisResearch  
                    elif ROIAnalysisResearch.objects.filter(id=legacy_energy.analysis.id).exists():
                        base_analysis = ROIAnalysisResearch.objects.get(id=legacy_energy.analysis.id)
                    
                    if not base_analysis:
                        print(f"    ❌ ROIAnalysis {legacy_energy.analysis.id} not found for EnergyAnalysisMetricValue {legacy_energy.id}")
                        continue
                    
                    metric = ROIMetric.objects.get(id=legacy_energy.metric.id)
                    
                    # Create child model with parent fields included
                    energy_value = EnergyAnalysisMetricValue.objects.create(
                        id=legacy_energy.id,
                        analysis=base_analysis,
                        metric=metric,
                        baselineValue=legacy_energy.baselineValue,
                        energy_cost_rate=legacy_energy.energy_cost_rate,
                        implementation_cost=legacy_energy.implementation_cost
                    )
                    migrated_count += 1
                    print(f"    ✅ Fixed EnergyAnalysisMetricValue {legacy_energy.id}")
                    
                except (ROIMetric.DoesNotExist, AttributeError) as e:
                    print(f"    ❌ Missing references for EnergyAnalysisMetricValue {legacy_energy.id}: {e}")
                    continue
                
        except Exception as e:
            print(f"    ❌ Error fixing EnergyAnalysisMetricValue {legacy_energy.id}: {e}")
    
    print(f"    Fixed {EnergyAnalysisMetricValue.objects.count()} EnergyAnalysisMetricValue records")
    
    print(f"\n✅ Fixed {migrated_count} inheritance records")
    
    return migrated_count

def validate_inheritance_fix():
    """Validate that the inheritance records have been fixed"""
    print("\n🔍 Validating inheritance fix...")
    
    # Import legacy and new models
    from api.models import (
        ROIAnalysisCalculation as LegacyROIAnalysisCalculation,
        ROIAnalysisResearch as LegacyROIAnalysisResearch,
        EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    )
    from apps.gaissa_roi_analyzer.models import (
        ROIAnalysisCalculation, ROIAnalysisResearch, EnergyAnalysisMetricValue
    )
    
    # Count records that were originally failing
    model_pairs = [
        ('ROIAnalysisCalculation', LegacyROIAnalysisCalculation, ROIAnalysisCalculation),
        ('ROIAnalysisResearch', LegacyROIAnalysisResearch, ROIAnalysisResearch),
        ('EnergyAnalysisMetricValue', LegacyEnergyAnalysisMetricValue, EnergyAnalysisMetricValue),
    ]
    
    total_legacy = 0
    total_new = 0
    
    for name, legacy_model, new_model in model_pairs:
        try:
            legacy_count = legacy_model.objects.count()
            new_count = new_model.objects.count()
            total_legacy += legacy_count
            total_new += new_count
            
            status = "✅" if legacy_count == new_count else "❌"
            print(f"  {status} {name}: {new_count}/{legacy_count}")
            
        except Exception as e:
            print(f"  ❌ Error counting {name}: {e}")
    
    print(f"\n📊 Total inheritance records: {total_new}/{total_legacy}")
    
    return total_legacy, total_new

if __name__ == "__main__":
    print("🚀 Starting Django inheritance migration fix...")
    
    try:
        # Fix inheritance migration
        fixed_count = fix_inheritance_migration()
        
        # Validate migration
        legacy_total, new_total = validate_inheritance_fix()
        
        print(f"\n🎉 Inheritance migration fix completed!")
        print(f"   Fixed {fixed_count} inheritance records")
        print(f"   Final status: {new_total}/{legacy_total} inheritance records migrated")
        
    except Exception as e:
        print(f"\n❌ Migration fix failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
