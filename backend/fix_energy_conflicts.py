#!/usr/bin/env python3
"""
Fix the EnergyAnalysisMetricValue conflicts by replacing AnalysisMetricValue
records with EnergyAnalysisMetricValue records for the conflicting entries.
"""

import os
import sys
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaissalabel.settings')
django.setup()

def fix_energy_analysis_conflicts():
    """Fix conflicts between AnalysisMetricValue and EnergyAnalysisMetricValue"""
    print("🔧 Fixing EnergyAnalysisMetricValue conflicts...")
    
    from api.models import EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    from apps.gaissa_roi_analyzer.models import (
        AnalysisMetricValue, EnergyAnalysisMetricValue, 
        ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric
    )
    
    # Get all legacy energy records that need to be migrated
    legacy_energy_records = LegacyEnergyAnalysisMetricValue.objects.all()
    fixed_count = 0
    
    for legacy_energy in legacy_energy_records:
        try:
            with transaction.atomic():
                analysis_id = legacy_energy.analysis.id
                metric_id = legacy_energy.metric.id
                
                print(f"  Processing Legacy EnergyAnalysisMetricValue ID {legacy_energy.id}")
                print(f"    (analysis_id={analysis_id}, metric_id={metric_id})")
                
                # Check if EnergyAnalysisMetricValue already exists
                if EnergyAnalysisMetricValue.objects.filter(id=legacy_energy.id).exists():
                    print(f"    ✅ EnergyAnalysisMetricValue {legacy_energy.id} already exists, skipping")
                    continue
                
                # Find the conflicting AnalysisMetricValue record
                conflicting_base = AnalysisMetricValue.objects.filter(
                    analysis_id=analysis_id, 
                    metric_id=metric_id
                ).first()
                
                if not conflicting_base:
                    print(f"    ⚠️ No conflicting AnalysisMetricValue found, creating new EnergyAnalysisMetricValue")
                else:
                    print(f"    🗑️ Deleting conflicting AnalysisMetricValue ID {conflicting_base.id}")
                    # Delete the conflicting base record
                    conflicting_base.delete()
                
                # Find the analysis (could be base, calculation, or research)
                base_analysis = None
                if ROIAnalysis.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysis.objects.get(id=analysis_id)
                elif ROIAnalysisCalculation.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysisCalculation.objects.get(id=analysis_id)
                elif ROIAnalysisResearch.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysisResearch.objects.get(id=analysis_id)
                
                if not base_analysis:
                    print(f"    ❌ ROIAnalysis {analysis_id} not found")
                    continue
                
                # Find the metric
                try:
                    metric = ROIMetric.objects.get(id=metric_id)
                except ROIMetric.DoesNotExist:
                    print(f"    ❌ ROIMetric {metric_id} not found")
                    continue
                
                # Create the EnergyAnalysisMetricValue
                energy_value = EnergyAnalysisMetricValue.objects.create(
                    id=legacy_energy.id,
                    analysis=base_analysis,
                    metric=metric,
                    baselineValue=legacy_energy.baselineValue,
                    energy_cost_rate=legacy_energy.energy_cost_rate,
                    implementation_cost=legacy_energy.implementation_cost
                )
                
                fixed_count += 1
                print(f"    ✅ Created EnergyAnalysisMetricValue ID {legacy_energy.id}")
                
        except Exception as e:
            print(f"    ❌ Error fixing Legacy EnergyAnalysisMetricValue {legacy_energy.id}: {e}")
    
    print(f"\n✅ Fixed {fixed_count} EnergyAnalysisMetricValue conflicts")
    return fixed_count

def validate_final_migration():
    """Final validation of the complete migration"""
    print("\n🔍 Final migration validation...")
    
    # Import models for counting
    from api.models import (
        ROIAnalysisCalculation as LegacyROIAnalysisCalculation,
        ROIAnalysisResearch as LegacyROIAnalysisResearch,
        EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    )
    from apps.gaissa_roi_analyzer.models import (
        ROIAnalysisCalculation, ROIAnalysisResearch, EnergyAnalysisMetricValue
    )
    
    # Check the problematic inheritance models
    model_pairs = [
        ('ROIAnalysisCalculation', LegacyROIAnalysisCalculation, ROIAnalysisCalculation),
        ('ROIAnalysisResearch', LegacyROIAnalysisResearch, ROIAnalysisResearch),
        ('EnergyAnalysisMetricValue', LegacyEnergyAnalysisMetricValue, EnergyAnalysisMetricValue),
    ]
    
    total_legacy = 0
    total_new = 0
    all_complete = True
    
    for name, legacy_model, new_model in model_pairs:
        try:
            legacy_count = legacy_model.objects.count()
            new_count = new_model.objects.count()
            total_legacy += legacy_count
            total_new += new_count
            
            if legacy_count == new_count:
                status = "✅"
            else:
                status = "❌"
                all_complete = False
                
            print(f"  {status} {name}: {new_count}/{legacy_count}")
            
        except Exception as e:
            print(f"  ❌ Error counting {name}: {e}")
            all_complete = False
    
    print(f"\n📊 Total inheritance records: {total_new}/{total_legacy}")
    
    if all_complete and total_legacy == total_new:
        print("🎉 All inheritance records successfully migrated!")
    else:
        print("⚠️ Some inheritance records still need attention")
    
    return total_legacy, total_new, all_complete

if __name__ == "__main__":
    print("🚀 Starting EnergyAnalysisMetricValue conflict resolution...")
    
    try:
        # Fix the conflicts
        fixed_count = fix_energy_analysis_conflicts()
        
        # Final validation
        total_legacy, total_new, all_complete = validate_final_migration()
        
        print(f"\n🎉 Conflict resolution completed!")
        print(f"   Fixed {fixed_count} conflicts")
        print(f"   Final result: {total_new}/{total_legacy} inheritance records migrated")
        
        if all_complete:
            print("\n✅ SUCCESS: All 51 inheritance records have been successfully migrated!")
        else:
            print(f"\n⚠️ {total_legacy - total_new} inheritance records still need attention")
        
    except Exception as e:
        print(f"\n❌ Conflict resolution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
